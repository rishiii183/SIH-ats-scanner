import sys
import os
import time
import requests
import json
from pptx import Presentation
from pptx.util import Inches

# Create realistic 6-slide PPTX file
deck_filename = "real_smoke_test_deck.pptx"
prs = Presentation()

slides_content = [
    ("Title Slide", "AI-Based Smart Traffic Management System for Urban Cities\nTeam CodeCraft | Problem Statement ID: SIH26101"),
    ("Problem Statement", "Problem Statement:\nMetropolitan intersections experience heavy traffic congestion leading to emergency vehicle delays and higher fuel emissions."),
    ("Proposed Solution", "Proposed Solution:\nAn adaptive traffic signal control system driven by real-time video analytics and computer vision."),
    ("Technical Approach", "Technical Approach:\nBuilt with Python, FastAPI backend microservices, PostgreSQL database with pgvector, and YOLOv8 object detection model."),
    ("Impact & Benefits", "Impact & Benefits:\n- 35% reduction in signal wait times.\n- Automated emergency vehicle priority routing.\n- 20% lower fuel consumption at urban intersections."),
    ("References & Team", "References & Team Contact:\nTeam Lead: lead@codecraft.org\nReferences: IEEE 2024 Smart Cities Traffic Analytics Paper.")
]

for title, content in slides_content:
    blank_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(blank_layout)
    tb = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(5))
    p = tb.text_frame.add_paragraph()
    p.text = f"{title}\n\n{content}"

prs.save(deck_filename)

print("Saved realistic 6-slide test presentation:", deck_filename)

# 1. Upload via HTTP POST to live FastAPI server
url = "http://127.0.0.1:8000/api/v1/submissions/upload"
with open(deck_filename, "rb") as f:
    files = {"file": (deck_filename, f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
    data = {"ps_id": "SIH26101"}
    resp = requests.post(url, files=files, data=data)

print("\nUpload HTTP Response Code:", resp.status_code)
upload_json = resp.json()
print("Upload Response JSON:")
print(json.dumps(upload_json, indent=2))

sub_id = upload_json.get("submission_id")

# 2. Poll Status
status_url = f"http://127.0.0.1:8000/api/v1/submissions/{sub_id}/status"
report_url = f"http://127.0.0.1:8000/api/v1/submissions/{sub_id}/report"

for attempt in range(15):
    time.sleep(1.0)
    st_resp = requests.get(status_url).json()
    print(f"Polling Status ({attempt+1}s): {st_resp.get('status')} - {st_resp.get('progress_step')} ({st_resp.get('progress_pct')}%)")
    if st_resp.get("status") == "completed":
        break

# 3. Fetch Final Report
rep_resp = requests.get(report_url)
print("\nFinal Report HTTP Status:", rep_resp.status_code)
report = rep_resp.json()
print("\n" + "=" * 80)
print("EXACT REAL REPORT RESPONSE FROM LIVE DEPLOYED URL:")
print("=" * 80)
print(json.dumps(report, indent=2))

# Cleanup temporary upload file
if os.path.exists(deck_filename):
    os.remove(deck_filename)
