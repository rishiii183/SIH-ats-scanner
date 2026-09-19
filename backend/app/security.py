import os
import re
from typing import Optional, Dict, Any, Tuple
from fastapi import UploadFile, HTTPException, Header
from app.config import settings

# Magic Bytes Signatures
# PPTX is a ZIP container: starts with PK\x03\x04 (0x50, 0x4B, 0x03, 0x04)
# PDF starts with %PDF- (0x25, 0x50, 0x44, 0x46, 0x2D)
MAGIC_SIGNATURES = {
    "pptx": [b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"],
    "pdf": [b"%PDF-"]
}

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes file name to prevent path traversal attacks and illegal characters.
    """
    cleaned = os.path.basename(filename)
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]", "_", cleaned)
    return cleaned or "presentation_deck.pptx"

async def validate_uploaded_file(file: UploadFile) -> Tuple[str, str, bytes]:
    """
    Performs production-grade validation:
    1. Filename sanitization
    2. File extension check
    3. File size limit enforcement (default 25MB)
    4. Magic-byte header verification to prevent disguised malicious binaries.
    
    Returns (sanitized_filename, extension, file_bytes)
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
        
    return clean_name, ext, content

def extract_user_from_auth_header(authorization: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Extracts user details from Supabase JWT Bearer token if provided.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
        
    token = authorization.split("Bearer ", 1)[1].strip()
    if not token:
        return None
        
    # Optional Supabase user resolution
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
    except Exception as e:
        # Silently degrade gracefully for public / guest evaluations
        pass
        
    return None
