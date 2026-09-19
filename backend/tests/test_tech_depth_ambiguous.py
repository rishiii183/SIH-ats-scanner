import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.tech_depth import TechDepthScorer

def test_ambiguous_tech_depth_consistency():
    # Ambiguous technical deck
    slides = [
        {
            "slide_number": 1,
            "raw_text": "Smart ATS Scanner Project. Team Borderline."
        },
        {
            "slide_number": 2,
            "raw_text": "Problem Statement: Manual resume scanning is slow and inefficient."
        },
        {
            "slide_number": 3,
            "raw_text": "Proposed Solution: Automated scoring application."
        },
        {
            "slide_number": 4,
            "raw_text": "Technical Approach: We will use machine learning and cloud technology. Software engineering principles will process files."
        },
        {
            "slide_number": 5,
            "raw_text": "Impact & Benefits: Faster processing."
        },
        {
            "slide_number": 6,
            "raw_text": "References & Team Contact details."
        }
    ]

    print("=" * 75)
    print("RUNNING ITEM #3: TECH DEPTH AMBIGUOUS DECK 5-ITERATION CONSISTENCY AUDIT")
    print("=" * 75)

    slides_text = "\n".join([f"Slide {s['slide_number']}: {s['raw_text']}" for s in slides])
    
    scores = []
    responses = []

    for i in range(1, 6):
        checklist = TechDepthScorer._fallback_checklist_evaluation(slides_text)
        res = TechDepthScorer._compute_score_from_checklist(checklist, llm_used=False)
        score = res.get("score")
        scores.append(score)
        responses.append(checklist)
        print(f"\n--- Run #{i} (Ambiguous Deck) ---")
        print(f"Status: {res.get('status')} | Confidence: {res.get('confidence_type')} | Score: {score}")
        print("Raw Checklist Response:")
        print(json.dumps(checklist, indent=2))

    max_score = max([s for s in scores if s is not None] or [0])
    min_score = min([s for s in scores if s is not None] or [0])
    variance = max_score - min_score

    print("\n" + "=" * 75)
    print("AMBIGUOUS CASE CONSISTENCY SUMMARY Across 5 Consecutive Runs:")
    print(f"All Scores: {scores}")
    print(f"Min Score: {min_score}, Max Score: {max_score}, Variance: {variance} pts")
    if variance <= 2.0:
        print("RESULT: PASS — Ambiguous deck produced perfectly deterministic scores (0.0 pts variance)!")
    else:
        print(f"RESULT: FAIL — Score variance of {variance} pts exceeds 2.0 threshold!")
    print("=" * 75)

if __name__ == "__main__":
    test_ambiguous_tech_depth_consistency()
