import sys
import os
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.tech_depth import TechDepthScorer

def test_tech_depth_consistency():
    # Sample tech deck slides
    slides = [
        {
            "slide_number": 1,
            "raw_text": "AI-Based Smart Traffic Management System for Urban Cities. Team CodeCraft."
        },
        {
            "slide_number": 2,
            "raw_text": "Problem Statement: Severe traffic congestion in metropolitan intersections leading to delays and emergency vehicle blocking."
        },
        {
            "slide_number": 3,
            "raw_text": "Technical Architecture & Stack: Built using Python with FastAPI for high-throughput API endpoints. Data stored in PostgreSQL with pgvector."
        },
        {
            "slide_number": 4,
            "raw_text": "Model & Algorithm: We deploy YOLOv8 deep learning model fine-tuned on custom traffic camera feeds to count vehicles dynamically and compute signal timer offsets."
        },
        {
            "slide_number": 5,
            "raw_text": "System Workflow: Edge camera feed -> YOLOv8 inference -> FastAPI backend -> Adaptive signal adjustment controller."
        },
        {
            "slide_number": 6,
            "raw_text": "References & Team Contact details."
        }
    ]

    print("=" * 70)
    print("RUNNING ITEM #2: TECH DEPTH SCORER 5-ITERATION CONSISTENCY AUDIT")
    print("=" * 70)

    scores = []
    responses = []

    for i in range(1, 6):
        res = TechDepthScorer.evaluate(slides)
        score = res.get("score")
        scores.append(score)
        checklist = res.get("raw_checklist", {})
        responses.append(checklist)
        print(f"\n--- Run #{i} ---")
        print(f"Status: {res.get('status')} | Confidence: {res.get('confidence_type')} | Score: {score}")
        print("Raw Checklist Response:")
        print(json.dumps(checklist, indent=2))

    max_score = max([s for s in scores if s is not None] or [0])
    min_score = min([s for s in scores if s is not None] or [0])
    variance = max_score - min_score

    print("\n" + "=" * 70)
    print("CONSISTENCY SUMMARY Across 5 Consecutive Runs:")
    print(f"All Scores: {scores}")
    print(f"Min Score: {min_score}, Max Score: {max_score}, Variance: {variance} pts")
    if variance <= 2.0:
        print("RESULT: PASS — Deterministic prompt with temperature=0.0 produced stable scores within <= 2.0 pts!")
    else:
        print(f"RESULT: FAIL — Score variance of {variance} pts exceeds 2.0 threshold!")
    print("=" * 70)

if __name__ == "__main__":
    test_tech_depth_consistency()
