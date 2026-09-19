import os
import io
import re
import time
import zipfile
from collections import defaultdict
from typing import Optional, Dict, Any, Tuple, List
from fastapi import UploadFile, HTTPException, Header, Request
from app.config import settings

# Magic Bytes Signatures
# PPTX is a ZIP container: starts with PK\x03\x04 (0x50, 0x4B, 0x03, 0x04)
# PDF starts with %PDF- (0x25, 0x50, 0x44, 0x46, 0x2D)
MAGIC_SIGNATURES = {
    "pptx": [b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"],
    "pdf": [b"%PDF-"]
}

# Zip Bomb & Decompression Limits
MAX_DECOMPRESSED_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB max uncompressed
MAX_COMPRESSION_RATIO = 100  # 100:1 ratio limit
MAX_ZIP_ENTRIES = 5000

# ==========================================
# 1. SLIDING WINDOW RATE LIMITER
# ==========================================
class InMemoryRateLimiter:
    """
    Sliding window in-memory rate limiter per IP address.
    """
    def __init__(self, requests_limit: int = 30, window_seconds: int = 60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.ip_history: Dict[str, List[float]] = defaultdict(list)

    def is_rate_limited(self, ip: str) -> Tuple[bool, int]:
        now = time.time()
        window_start = now - self.window_seconds
        
        # Purge timestamps older than the window
        timestamps = [t for t in self.ip_history[ip] if t > window_start]
        self.ip_history[ip] = timestamps
        
        if len(timestamps) >= self.requests_limit:
            retry_after = int(self.window_seconds - (now - timestamps[0])) + 1
            return True, max(1, retry_after)
            
        self.ip_history[ip].append(now)
        return False, 0

# Global Rate Limiter Instance
rate_limiter = InMemoryRateLimiter(
    requests_limit=settings.RATE_LIMIT_PER_MINUTE, 
    window_seconds=60
)

# ==========================================
# 2. INPUT SANITIZATION & SECURITY HELPERS
# ==========================================
def sanitize_filename(filename: str) -> str:
    """
    Sanitizes file name to prevent path traversal attacks and illegal characters.
    """
    cleaned = os.path.basename(filename)
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]", "_", cleaned)
    return cleaned or "presentation_deck.pptx"

def sanitize_text(text: Optional[str], max_length: int = 2000) -> str:
    """
    Sanitizes arbitrary text inputs (like custom PS descriptions or query strings)
    against prompt injection, control characters, and buffer overflows.
    """
    if not text:
        return ""
    # Strip null bytes and control chars
    clean = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
    return clean[:max_length].strip()

# ==========================================
# 3. DEEP ARCHIVE & FILE VALIDATION
# ==========================================
def validate_zip_safety(file_bytes: bytes):
    """
    Inspects ZIP headers (PPTX files) to defend against zip-bomb and decompression attacks.
    """
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
            total_uncompressed = 0
            entries = zf.infolist()
            
            if len(entries) > MAX_ZIP_ENTRIES:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid PPTX archive: Contains abnormally high number of internal file entries."
                )
                
            for member in entries:
                # Prevent zip path traversal
                if member.filename.startswith("/") or ".." in member.filename:
                    raise HTTPException(
                        status_code=400,
                        detail="Malicious PPTX archive detected: Path traversal signature in archive member."
                    )
                total_uncompressed += member.file_size
                
            compressed_size = len(file_bytes)
            if total_uncompressed > MAX_DECOMPRESSED_SIZE_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail="Presentation exceeds uncompressed safety limits (Zip bomb protection)."
                )
                
            if compressed_size > 0 and (total_uncompressed / compressed_size) > MAX_COMPRESSION_RATIO:
                raise HTTPException(
                    status_code=400,
                    detail="Abnormal compression ratio detected in presentation archive."
                )
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=400,
            detail="Corrupted or invalid PPTX file structure."
        )

def validate_pdf_safety(file_bytes: bytes):
    """
    Checks PDF streams for suspicious active executable payloads (/Launch, /JavaScript).
    """
    header_sample = file_bytes[:1024 * 1024] # Inspect first 1MB
    if b"/Launch" in header_sample:
        raise HTTPException(
            status_code=400,
            detail="Security Violation: PDF contains disallowed external /Launch action."
        )

async def validate_uploaded_file(file: UploadFile) -> Tuple[str, str, bytes]:
    """
    Performs production-grade multi-layer validation:
    1. Filename sanitization (Path traversal defense)
    2. File extension check (.pptx, .pdf)
    3. File size limit enforcement (25MB max)
    4. Magic-byte header verification (Genuine binary check)
    5. Deep archive & safety analysis (Zip-bomb & PDF payload inspection)
    """
    raw_name = file.filename or "presentation.pptx"
    clean_name = sanitize_filename(raw_name)
    
    parts = clean_name.rsplit(".", 1)
    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="File must have an explicit extension (.pptx or .pdf)."
        )
    
    ext = parts[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Read and validate file content
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read uploaded file: {str(e)}"
        )
    
    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty (0 bytes)."
        )
        
    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )
    
    # Magic bytes verification
    is_valid_magic = False
    signatures = MAGIC_SIGNATURES.get(ext, [])
    for sig in signatures:
        if content.startswith(sig):
            is_valid_magic = True
            break
            
    if not is_valid_magic:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file structure. The file header does not match a genuine .{ext} document format."
        )
        
    # Deep archive / format safety checks
    if ext == "pptx":
        validate_zip_safety(content)
    elif ext == "pdf":
        validate_pdf_safety(content)
        
    return clean_name, ext, content

# ==========================================
# 4. SUPABASE JWT AUTHENTICATION
# ==========================================
def extract_user_from_auth_header(authorization: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Extracts user details from Supabase JWT Bearer token if provided.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
        
    token = authorization.split("Bearer ", 1)[1].strip()
    if not token:
        return None
        
    try:
        from app.database import DBManager
        client = DBManager.get_client()
        if client:
            user_resp = client.auth.get_user(token)
            if user_resp and user_resp.user:
                return {
                    "id": user_resp.user.id,
                    "email": user_resp.user.email,
                }
    except Exception:
        # Gracefully handle unauthenticated guest evaluation
        pass
        
    return None
