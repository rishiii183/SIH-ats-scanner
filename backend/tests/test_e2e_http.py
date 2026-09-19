import sys
import os
import io

# Add backend root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def test_e2e_http_flow():
    client = TestClient(app)

    # Minimal valid PDF binary header & content
    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kinds [ /Page ] /Count 4 /Kids [ 3 0 R 4 0 R 5 0 R 6 0 R ] >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /Contents 7 0 R >> endobj\n"
        b"4 0 obj << /Type /Page /Parent 2 0 R /Contents 8 0 R >> endobj\n"
        b"5 0 obj << /Type /Page /Parent 2 0 R /Contents 9 0 R >> endobj\n"
        b"6 0 obj << /Type /Page /Parent 2 0 R /Contents 10 0 R >> endobj\n"
        b"7 0 obj << /Length 120 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Title Slide: AI Traffic Management. Team Innovators. Problem Statement: SIH26101.) Tj ET\n"
        b"endstream endobj\n"
        b"8 0 obj << /Length 130 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Problem Statement & Challenge: Traffic congestion in smart cities causes delays for ambulances.) Tj ET\n"
        b"endstream endobj\n"
        b"9 0 obj << /Length 150 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Proposed Solution & Tech Stack: Python, OpenCV, YOLOv8, FastAPI, PostgreSQL database with pgvector, Redis, Docker.) Tj ET\n"
        b"endstream endobj\n"
        b"10 0 obj << /Length 130 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Impact & References & Team: Reduces delays by 35%. Contact team@example.com.) Tj ET\n"
        b"endstream endobj\n"
        b"xref\n0 11\n"
        b"0000000000 65535 f \n"
        b"trailer << /Size 11 /Root 1 0 R >>\n"
        b"startxref\n700\n%%EOF"
    )

    print("--- 1. HTTP POST /api/v1/submissions/upload ---")
    files = {"file": ("sih_deck_sample.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    data = {"ps_id": "SIH26101"}
    
    upload_res = client.post("/api/v1/submissions/upload", files=files, data=data)
    print("HTTP Status:", upload_res.status_code)
    print("Upload Payload:", upload_res.json())

    assert upload_res.status_code == 200
    sub_id = upload_res.json()["submission_id"]

    print("\n--- 2. HTTP GET /api/v1/submissions/{sub_id}/status ---")
    status_res = client.get(f"/api/v1/submissions/{sub_id}/status")
    print("HTTP Status:", status_res.status_code)
    print("Status Payload:", status_res.json())

    print("\n--- 3. HTTP GET /api/v1/submissions/{sub_id}/report ---")
    report_res = client.get(f"/api/v1/submissions/{sub_id}/report")
    print("HTTP Status:", report_res.status_code)
    print("Report Payload:", report_res.json())

if __name__ == "__main__":
    test_e2e_http_flow()
