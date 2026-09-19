import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.aggregator import ScoreAggregator
from app.database import DBManager
from tests.test_tech_depth_consistency import test_tech_depth_consistency
from tests.test_golden_set import run_golden_set_tests

def run_defensibility_verification():
    print("=" * 80)
    print("DEFENSIBILITY HARDENING VERIFICATION SUITE")
    print("=" * 80)

    # Sample test deck with real content
    slides = [
        {
            "slide_number": 1,
            "raw_text": "AI-Based Smart Traffic Management System for Urban Cities. Team CodeCraft.",
            "bullet_count": 0
        },
        {
            "slide_number": 2,
            "raw_text": "Problem Statement: Traffic congestion at metropolitan intersections leads to emergency delays.",
            "bullet_count": 2
        },
        {
            "slide_number": 3,
            "raw_text": "Proposed Solution: Dynamic signal adjustment using camera feeds.",
            "bullet_count": 2
        },
        {
            "slide_number": 4,
            "raw_text": "Technical Approach: Built with Python, FastAPI, PostgreSQL database with pgvector, and YOLOv8 object detection model.",
            "bullet_count": 3
        },
        {
            "slide_number": 5,
            "raw_text": "Impact & Benefits: 35% congestion reduction.",
            "bullet_count": 2
        },
        {
            "slide_number": 6,
            "raw_text": "References & Team Contact: contact@codecraft.org",
            "bullet_count": 1
        },
        {
            "slide_number": 7,
            "raw_text": "Extra Slide: lorem ipsum placeholder text sample problem statement.",
            "bullet_count": 9
        }
    ]

    print("\n--- ITEM 1, 5, 6: REASON SCHEMA, CONFIDENCE TYPE, AND DISCLAIMER VERIFICATION ---")
    report = ScoreAggregator.process_submission(
        slides=slides,
        ps_title="AI-Based Smart Traffic Management System for Urban Cities",
        ps_description="Optimize traffic light signals using computer vision."
    )

    print(f"\nOverall Score: {report['overall_score']}")
    print(f"Verdict Text: {report['verdict_text']}")
    print(f"\nExact Disclaimer Text (Item #6):\n\"{report['disclaimer']}\"")

    print("\nCategory Breakdown Cards with Confidence Type & Reason Schemas (Item #1 & #5):")
    for cat_key, cat_data in report['category_breakdown'].items():
        print(f"\n>>> Category: {cat_key.upper()} | Status: {cat_data['status']} | Confidence Type: {cat_data['confidence_type']} | Score: {cat_data['score']}")
        print("Reasons:")
        for r in cat_data.get('reasons', []):
            print(json.dumps(r, indent=2))

    print("\n--- ITEM 4: FULL AUDIT TRAIL PERSISTENCE & RECONSTRUCTION ---")
    sub_id = "test-audit-sub-12345"
    extracted_meta = [
        {"slide_number": s["slide_number"], "word_count": len(s["raw_text"].split()), "bullet_count": s.get("bullet_count", 0), "text_snippet": s["raw_text"][:100]}
        for s in slides
    ]
    tech_breakdown = report.get("category_breakdown", {}).get("technical_depth", {})
    llm_audit = {
        "prompt": "Structured Checklist Audit (names_specific_framework_or_language, names_specific_database_or_storage, names_specific_model_or_algorithm, describes_architecture_or_workflow)",
        "raw_response": tech_breakdown.get("raw_checklist", {})
    }

    DBManager.save_audit_trail(
        sub_id=sub_id,
        rubric_config_id=report["rubric_config_id"],
        extracted_text_metadata={"slides": extracted_meta, "total_slides": len(slides)},
        llm_prompt_raw_response=llm_audit,
        weight_math_details=report["weight_math_details"]
    )

    retrieved_audit = DBManager.get_audit_trail(sub_id)
    print("\nRetrieved Audit Trail Record (Querying Back):")
    print(json.dumps(retrieved_audit, indent=2))

    print("\n--- ITEM 2: TECH DEPTH 5-RUN CONSISTENCY AUDIT ---")
    test_tech_depth_consistency()

    print("\n--- ITEM 3: GOLDEN-SET REGRESSION SUITE (8 SAMPLES) ---")
    run_golden_set_tests()

if __name__ == "__main__":
    run_defensibility_verification()
