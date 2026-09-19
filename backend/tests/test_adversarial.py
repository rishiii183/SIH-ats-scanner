import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.structure import StructureScorer
from app.scoring.clarity import ClarityScorer
from app.scoring.aggregator import ScoreAggregator
from app.database import DBManager

def test_adversarial_bad_deck():
    # Construct a deliberately bad 12-slide presentation
    bad_slides = []
    
    # Slide 1: Title
    bad_slides.append({
        "slide_number": 1,
        "raw_text": "Title Slide: Sample Idea. Team: Group A.",
        "word_count": 8,
        "bullet_count": 0,
        "image_count": 0
    })

    # Slide 2: Problem
    bad_slides.append({
        "slide_number": 2,
        "raw_text": "Problem Statement & Need: General problem description without details.",
        "word_count": 10,
        "bullet_count": 0,
        "image_count": 0
    })

    # Slide 3: Wall of text with 10 bullet points and 110 words
    wall_text = (
        "Proposed Solution & Overview: Point 1: We build a website. Point 2: We build a database. "
        "Point 3: We connect cloud servers. Point 4: We train a model. Point 5: We create UI screens. "
        "Point 6: We test performance. Point 7: We deploy to AWS. Point 8: We add security. "
        "Point 9: We manage logs. Point 10: We monitor performance. Point 11: We collect user metrics."
    )
    bad_slides.append({
        "slide_number": 3,
        "raw_text": wall_text,
        "word_count": 110,
        "bullet_count": 11,
        "image_count": 0  # Missing visual diagram on slide 3
    })

    # Slide 4: Tech Stack (Missing visual diagram on slide 4)
    bad_slides.append({
        "slide_number": 4,
        "raw_text": "Technical Approach & Tech Stack: Python, MySQL.",
        "word_count": 8,
        "bullet_count": 0,
        "image_count": 0
    })

    # Slide 5: Impact
    bad_slides.append({
        "slide_number": 5,
        "raw_text": "Impact & Benefits: Good outcomes for community.",
        "word_count": 7,
        "bullet_count": 0,
        "image_count": 0
    })

    # Slides 6 to 12: Filler slides to blow past 6-slide max limit, and MISSING References/Team slide!
    for i in range(6, 13):
        bad_slides.append({
            "slide_number": i,
            "raw_text": f"Extra Filler Slide {i}: Additional background text.",
            "word_count": 15,
            "bullet_count": 0,
            "image_count": 0
        })

    rubric_config = DBManager.get_active_rubric_config()

    print("--- 1. StructureScorer Adversarial Evaluation ---")
    struct_res = StructureScorer.evaluate(bad_slides, rubric_config)
    print("Structure Score:", struct_res["score"])
    print("Structure Reasons:")
    for r in struct_res["reasons"]:
        print("  - Deduction:", r["deduction"], "| Message:", r["message"])

    print("\n--- 2. ClarityScorer Adversarial Evaluation ---")
    clarity_res = ClarityScorer.evaluate(bad_slides)
    print("Clarity Score:", clarity_res["score"])
    print("Clarity Reasons:")
    for r in clarity_res["reasons"]:
        print("  - Deduction:", r["deduction"], "| Message:", r["message"])

    print("\n--- 3. Full ScoreAggregator Adversarial Evaluation ---")
    report = ScoreAggregator.process_submission(
        slides=bad_slides,
        ps_title="AI-Based Smart Traffic Management System for Urban Cities",
        ps_description="Develop real-time traffic signal optimization system.",
        rubric_config=rubric_config
    )

    print("Overall Score:", report["overall_score"])
    print("Verdict Text:", report["verdict_text"])
    print("Evaluation Completeness:", report["evaluation_completeness"])
    print("Breakdown:", report["category_breakdown"])

if __name__ == "__main__":
    test_adversarial_bad_deck()
