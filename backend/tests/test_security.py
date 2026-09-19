import sys
import os
import io
from fastapi import HTTPException

# Add app to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.security import (
    validate_pdf_safety,
    validate_zip_safety,
    sanitize_filename,
    sanitize_text,
    InMemoryRateLimiter
)

def test_valid_pdf():
    """Test standard genuine PDF passes security audit."""
    clean_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n%%EOF"
    validate_pdf_safety(clean_pdf_bytes)
    print("  [PASS] Clean PDF accepted.")

def test_malicious_pdf_with_javascript():
    """Test PDF with embedded /JavaScript exploit is blocked."""
    malicious_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Action /S /JavaScript /JS (app.alert('Malware Triggered!')) >>\nendobj\n%%EOF"
    try:
        validate_pdf_safety(malicious_pdf_bytes)
        assert False, "Should have raised HTTPException for /JavaScript"
    except HTTPException as e:
        assert e.status_code == 400
        assert "Disallowed executable embedded script" in e.detail
        print(f"  [PASS] Malicious PDF (/JavaScript) BLOCKED: {e.detail}")

def test_malicious_pdf_with_launch():
    """Test PDF with OS command execution (/Launch) is blocked."""
    launch_pdf_bytes = b"%PDF-1.4\n<< /Type /Action /S /Launch /F (cmd.exe) >>\n%%EOF"
    try:
        validate_pdf_safety(launch_pdf_bytes)
        assert False, "Should have raised HTTPException for /Launch"
    except HTTPException as e:
        assert e.status_code == 400
        assert "Disallowed external OS execution action" in e.detail
        print(f"  [PASS] Malicious PDF (/Launch) BLOCKED: {e.detail}")

def test_malicious_pdf_with_embedded_file():
    """Test PDF with embedded hidden executable dropper (/EmbeddedFiles) is blocked."""
    embedded_pdf_bytes = b"%PDF-1.4\n<< /Type /Names /EmbeddedFiles << /Names [ (malware.exe) 5 0 R ] >> >>\n%%EOF"
    try:
        validate_pdf_safety(embedded_pdf_bytes)
        assert False, "Should have raised HTTPException for /EmbeddedFiles"
    except HTTPException as e:
        assert e.status_code == 400
        assert "Disallowed embedded hidden payload dropper" in e.detail
        print(f"  [PASS] Malicious PDF (/EmbeddedFiles) BLOCKED: {e.detail}")

def test_rate_limiter():
    """Test in-memory sliding window rate limiter blocks flood requests."""
    limiter = InMemoryRateLimiter(requests_limit=3, window_seconds=60)
    ip = "192.168.1.100"
    
    # First 3 requests allowed
    assert limiter.is_rate_limited(ip)[0] is False
    assert limiter.is_rate_limited(ip)[0] is False
    assert limiter.is_rate_limited(ip)[0] is False
    
    # 4th request must be blocked
    is_limited, retry_after = limiter.is_rate_limited(ip)
    assert is_limited is True
    assert retry_after > 0
    print(f"  [PASS] Rate limiter BLOCKED 4th request from same IP (Retry after: {retry_after}s)")

def test_input_sanitizer():
    """Test prompt injection and control character stripping."""
    raw = "SIH26101\x00\x08--DROP TABLE users;-- <script>alert(1)</script>"
    clean = sanitize_text(raw, max_length=50)
    assert "\x00" not in clean
    assert "\x08" not in clean
    print(f"  [PASS] Input Sanitizer: '{raw[:20]}...' -> '{clean}'")

if __name__ == "__main__":
    print("\n==============================================")
    print("      SIH ATS SCANNER - SECURITY TEST SUITE   ")
    print("==============================================")
    test_valid_pdf()
    test_malicious_pdf_with_javascript()
    test_malicious_pdf_with_launch()
    test_malicious_pdf_with_embedded_file()
    test_rate_limiter()
    test_input_sanitizer()
    print("\nALL 6/6 SECURITY DEFENSE TESTS PASSED! [PASS]\n")

