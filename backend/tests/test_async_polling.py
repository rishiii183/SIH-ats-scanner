import sys
import os
import io
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def test_async_polling_behavior():
    client = TestClient(app)

    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kinds [ /Page ] /Count 4 /Kids [ 3 0 R 4 0 R 5 0 R 6 0 R ] >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /Contents 7 0 R >> endobj\n"
        b"4 0 obj << /Type /Page /Parent 2 0 R /Contents 8 0 R >> endobj\n"
        b"5 0 obj << /Type /Page /Parent 2 0 R /Contents 9 0 R >> endobj\n"
        b"6 0 obj << /Type /Page /Parent 2 0 R /Contents 10 0 R >> endobj\n"
        b"7 0 obj << /Length 120 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Title Slide: Smart City Traffic. Team AI. Problem Statement: SIH26101.) Tj ET\n"
        b"endstream endobj\n"
        b"8 0 obj << /Length 130 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Problem Statement: Urban traffic congestion control system.) Tj ET\n"
        b"endstream endobj\n"
        b"9 0 obj << /Length 150 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Proposed Solution: Python, OpenCV, YOLOv8, FastAPI, PostgreSQL pgvector, Redis, Docker.) Tj ET\n"
        b"endstream endobj\n"
        b"10 0 obj << /Length 130 >> stream\n"
        b"BT /F1 12 Tf 50 700 Td (Impact & References: Scalable. Contact: team@example.com) Tj ET\n"
        b"endstream endobj\n"
        b"xref\n0 11\n"
        b"0000000000 65535 f \n"
        b"trailer << /Size 11 /Root 1 0 R >>\n"
        b"startxref\n700\n%%EOF"
    )

    print("==================================================")
    print("      ASYNC BACKGROUND POLLING DEMO               ")
    print("==================================================")

    # 1. Upload
    files = {"file": ("sih_test_async.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    data = {"ps_id": "SIH26101"}
    
    start_time = time.time()
    upload_res = client.post("/api/v1/submissions/upload", files=files, data=data)
    upload_duration = (time.time() - start_time) * 1000

    print(f"1. POST /upload response code: {upload_res.status_code} (Duration: {upload_duration:.1f}ms)")
    upload_json = upload_res.json()
    sub_id = upload_json["submission_id"]
    print(f"   Initial status returned to client: status='{upload_json['status']}', submission_id='{sub_id}'")

    # 2. Immediate Status Check (Right after upload returns)
    status_res1 = client.get(f"/api/v1/submissions/{sub_id}/status")
    status_json1 = status_res1.json()
    print(f"2. Immediate GET /status response: status='{status_json1['status']}', step='{status_json1.get('progress_step')}', pct={status_json1.get('progress_pct')}%")

    # 3. Poll after delay
    print("3. Waiting 1.2s for background pipeline stage execution...")
    time.sleep(1.2)

    status_res2 = client.get(f"/api/v1/submissions/{sub_id}/status")
    status_json2 = status_res2.json()
    print(f"4. Polled GET /status response after delay: status='{status_json2['status']}', step='{status_json2.get('progress_step')}', pct={status_json2.get('progress_pct')}%")

if __name__ == "__main__":
    test_async_polling_behavior()
