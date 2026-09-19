import sys
import os
import io
import time
import threading
from pptx import Presentation
from pptx.util import Inches, Pt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def generate_real_6_slide_pptx() -> bytes:
    """
    Generates a realistic 6-slide OpenXML PPTX presentation file in memory.
    Contains realistic text paragraphs, section headings, and bullet points.
    """
    prs = Presentation()
    blank_layout = prs.slide_layouts[6]  # blank slide

    slides_content = [
        {
            "title": "Title Slide: Smart Urban Traffic Signal Optimizer",
            "body": "Team: Neural Hackers. Problem Statement ID: SIH26101. Theme: Smart Cities & Urban Infrastructure. Category: Software Track."
        },
        {
            "title": "Problem Statement & Need Analysis",
            "body": "Urban traffic congestion in Indian tier-1 and tier-2 metropolitan junctions causes severe economic productivity losses and ambulance transit delays. Fixed timer traffic signals cannot adapt to dynamic vehicle density spikes during peak hours, resulting in emergency vehicle blockage and excessive fuel consumption."
        },
        {
            "title": "Proposed Solution & Vision AI Architecture",
            "body": "We propose a real-time adaptive traffic signal control system powered by edge computer vision. CCTV camera feeds at quad-intersections are processed by lightweight object detection models to dynamically estimate queue lengths per lane. Priority routing green channels are automatically granted to approaching emergency ambulances."
        },
        {
            "title": "Technical Approach & Technology Stack",
            "body": "Tech Stack: Python 3.11, OpenCV, YOLOv8 object detection fine-tuned on custom Indian vehicle datasets, TensorRT optimization. Backend REST microservices built with FastAPI, PostgreSQL with pgvector spatial extension, Redis pub/sub caching layer, containerized via Docker and Kubernetes."
        },
        {
            "title": "Impact, Feasibility & Scalability",
            "body": "Reduces junction wait times by 35%. Decreases emergency vehicle response latency by 8 minutes. Scalable across 100+ municipal junctions using existing CCTV infrastructure with minimal hardware additions. Projected social ROI: 15x annual operational cost."
        },
        {
            "title": "References, Team & Mentor Details",
            "body": "Research Papers: IEEE Transactions on Intelligent Transportation Systems (2024). Team Lead: Raj Sharma (CS). Mentor: Dr. A. Kumar. Contact: team.neuralhackers@example.com."
        }
    ]

    for item in slides_content:
        slide = prs.slides.add_slide(blank_layout)
        txBox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(5))
        tf = txBox.text_frame
        
        p = tf.paragraphs[0]
        p.text = item["title"]
        p.font.size = Pt(22)
        p.font.bold = True

        p2 = tf.add_paragraph()
        p2.text = item["body"]
        p2.font.size = Pt(14)

    out = io.BytesIO()
    prs.save(out)
    out.seek(0)
    return out.read()

def test_real_concurrency():
    client = TestClient(app)
    pptx_bytes = generate_real_6_slide_pptx()
    print(f"Generated realistic PPTX deck: {len(pptx_bytes)} bytes across 6 slides.")

    results = {}
    lock = threading.Lock()

    def upload_worker(user_tag: str):
        t_start = time.perf_counter()
        files = {"file": (f"sih_real_{user_tag}.pptx", io.BytesIO(pptx_bytes), "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
        data = {"ps_id": "SIH26101"}

        res = client.post("/api/v1/submissions/upload", files=files, data=data)
        t_upload_done = time.perf_counter()

        if res.status_code == 200:
            sub_id = res.json()["submission_id"]
            
            # Poll status until completed
            t_poll_start = time.perf_counter()
            while True:
                status_res = client.get(f"/api/v1/submissions/{sub_id}/status")
                s_json = status_res.json()
                if s_json.get("status") == "completed":
                    t_completed = time.perf_counter()
                    break
                time.sleep(0.05)

            with lock:
                results[user_tag] = {
                    "sub_id": sub_id,
                    "t_start": t_start,
                    "t_upload_done": t_upload_done,
                    "t_completed": t_completed,
                    "upload_handler_ms": (t_upload_done - t_start) * 1000,
                    "total_pipeline_ms": (t_completed - t_start) * 1000,
                    "report": s_json.get("report")
                }

    print("==================================================")
    print("      REAL PPTX CONCURRENCY & LATENCY AUDIT       ")
    print("==================================================")

    thread_a = threading.Thread(target=upload_worker, args=("User_A",))
    thread_b = threading.Thread(target=upload_worker, args=("User_B",))

    t_global_start = time.perf_counter()
    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()
    t_global_end = time.perf_counter()

    res_a = results["User_A"]
    res_b = results["User_B"]

    print(f"\n1. REAL PROCESSING DURATION (PPTX Parsing + PyTorch Embedding Inference):")
    print(f"   - User A Upload Handler Duration: {res_a['upload_handler_ms']:.2f} ms")
    print(f"   - User A Total Pipeline Latency:  {res_a['total_pipeline_ms']:.2f} ms")
    print(f"   - User B Upload Handler Duration: {res_b['upload_handler_ms']:.2f} ms")
    print(f"   - User B Total Pipeline Latency:  {res_b['total_pipeline_ms']:.2f} ms")

    print(f"\n2. TIMESTAMPS & CONCURRENCY QUEUING ANALYSIS:")
    print(f"   - User A Upload Started:  +{res_a['t_start'] - t_global_start:.4f} s")
    print(f"   - User A Pipeline Finish: +{res_a['t_completed'] - t_global_start:.4f} s")
    print(f"   - User B Upload Started:  +{res_b['t_start'] - t_global_start:.4f} s")
    print(f"   - User B Pipeline Finish: +{res_b['t_completed'] - t_global_start:.4f} s")

    print(f"\n3. SAMPLE REPORT OUTPUT (User A):")
    print(f"   - Overall Score: {res_a['report']['overall_score']}")
    print(f"   - Verdict: {res_a['report']['verdict_text']}")

if __name__ == "__main__":
    test_real_concurrency()
