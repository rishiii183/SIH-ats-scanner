import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.structure import StructureScorer
from app.scoring.clarity import ClarityScorer
from app.scoring.ps_alignment import PSAlignmentScorer
from app.scoring.tech_depth import TechDepthScorer
from app.scoring.originality import OriginalityScorer
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

    # Slide 3: Wall of text with 11 bullet points and 110 words
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
        "image_count": 0
    })

    # Slide 4: Tech Stack
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

    # Slides 6 to 12: Filler slides exceeding 6-slide max limit and missing References/Team section
    for i in range(6, 13):
        bad_slides.append({
            "slide_number": i,
            "raw_text": f"Extra Filler Slide {i}: Additional background text.",
            "word_count": 15,
            "bullet_count": 0,
            "image_count": 0
        })

    rubric_config = DBManager.get_active_rubric_config()
    ps_title = "AI-Based Smart Traffic Management System for Urban Cities"
    ps_description = "Develop real-time traffic signal optimization system using computer vision and IoT sensors."

    print("==================================================")
    print("      ADVERSARIAL DECK SCORING AUDIT              ")
    print("==================================================")

    # 1. Structure
    struct_res = StructureScorer.evaluate(bad_slides, rubric_config)
    print(f"\n1. Structure & Format Compliance:")
    print(f"   Raw Score: {struct_res['score']} / 100")
    for r in struct_res['reasons']:
        print(f"   - Deduction: -{r['deduction']} pts | Message: {r['message']}")

    # 2. PS Alignment
    align_res = PSAlignmentScorer.evaluate(bad_slides, ps_title, ps_description)
    print(f"\n2. Problem Statement Alignment:")
    print(f"   Raw Score: {align_res['score']} / 100")
    print(f"   Cosine Similarity: {align_res.get('similarity_score', 0)}")
    for r in align_res['reasons']:
        print(f"   - Deduction: -{r['deduction']} pts | Message: {r['message']}")

    # 3. Clarity
    clarity_res = ClarityScorer.evaluate(bad_slides)
    print(f"\n3. Presentation Clarity:")
    print(f"   Raw Score: {clarity_res['score']} / 100")
    for r in clarity_res['reasons']:
        print(f"   - Deduction: -{r['deduction']} pts | Message: {r['message']}")

    # 4. Tech Depth & Originality Status
    tech_res = TechDepthScorer.evaluate(bad_slides, "")
    orig_res = OriginalityScorer.evaluate(bad_slides, 0)
    print(f"\n4. Technical Depth Status: {tech_res['status']} (Weight 0.0)")
    print(f"5. Originality Status: {orig_res['status']} (Weight 0.0)")

    # 5. Full Aggregator Evaluation
    report = ScoreAggregator.process_submission(
        slides=bad_slides,
        ps_title=ps_title,
        ps_description=ps_description,
        rubric_config=rubric_config
    )

    cb = report["category_breakdown"]
    s_score = cb["structure_format"]["score"]
    s_w = cb["structure_format"]["weight_applied"]
    
    a_score = cb["ps_alignment"]["score"]
    a_w = cb["ps_alignment"]["weight_applied"]

    c_score = cb["clarity"]["score"]
    c_w = cb["clarity"]["weight_applied"]

    print("\n==================================================")
    print("      STEP-BY-STEP AGGREGATOR ARITHMETIC          ")
    print("==================================================")
    print(f"Nominal active category weights sum: 0.15 (Struct) + 0.20 (Align) + 0.15 (Clarity) = 0.50")
    print(f"Renormalized Weight 1 (Structure):  0.15 / 0.50 = {s_w}")
    print(f"Renormalized Weight 2 (PS Align):   0.20 / 0.50 = {a_w}")
    print(f"Renormalized Weight 3 (Clarity):    0.15 / 0.50 = {c_w}")
    print("--------------------------------------------------")
    print(f"Component 1 (Structure):  {s_score} × {s_w} = {round(s_score * s_w, 2)}")
    print(f"Component 2 (PS Align):   {a_score} × {a_w} = {round(a_score * a_w, 2)}")
    print(f"Component 3 (Clarity):    {c_score} × {c_w} = {round(c_score * c_w, 2)}")
    print("--------------------------------------------------")
    calculated_sum = (s_score * s_w) + (a_score * a_w) + (c_score * c_w)
    print(f"Calculated Overall Score Sum: {s_score * s_w:.2f} + {a_score * a_w:.2f} + {c_score * c_w:.2f} = {calculated_sum:.2f} (Rounded: {round(calculated_sum, 1)})")
    print(f"Aggregator Reported Overall Score: {report['overall_score']}")
    print(f"Verdict Text: {report['verdict_text']}")

if __name__ == "__main__":
    test_adversarial_bad_deck()
