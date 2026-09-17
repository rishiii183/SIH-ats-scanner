import sys
import os

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.structure import StructureScorer
from app.scoring.clarity import ClarityScorer
from app.scoring.ps_alignment import PSAlignmentScorer
from app.scoring.tech_depth import TechDepthScorer
from app.scoring.originality import OriginalityScorer
from app.scoring.aggregator import ScoreAggregator

def test_scoring_pipeline():
    sample_slides = [
        {
            "slide_number": 1,
            "raw_text": "Title: AI Traffic Optimization. Team: Tech Hackers. Problem Statement ID: SIH26101. Theme: Smart Cities.",
            "word_count": 18,
            "bullet_count": 0,
            "image_count": 1
        },
        {
            "slide_number": 2,
            "raw_text": "Problem Statement & Challenge: Urban traffic congestion causes hours of delay. Emergency ambulances get trapped in traffic jams at smart city intersections.",
            "word_count": 22,
            "bullet_count": 2,
            "image_count": 0
        },
        {
            "slide_number": 3,
            "raw_text": "Proposed Solution: Real-time traffic light control using computer vision and edge IoT sensors. Priority signal routing for emergency vehicles.",
            "word_count": 20,
            "bullet_count": 3,
            "image_count": 1
        },
        {
            "slide_number": 4,
            "raw_text": "Technical Approach & Tech Stack: Python, OpenCV, YOLOv8 object detection model fine-tuned on urban vehicle datasets. FastAPI backend, PostgreSQL database with pgvector for spatial data, Redis caching layer, Docker containerization.",
            "word_count": 30,
            "bullet_count": 4,
            "image_count": 1
        },
        {
            "slide_number": 5,
            "raw_text": "Impact & Benefits: Reduces traffic wait times by 35%. Reduces ambulance arrival times by 8 minutes. Scalable across 100+ municipal smart city junctions.",
            "word_count": 24,
            "bullet_count": 3,
            "image_count": 1
        },
        {
            "slide_number": 6,
            "raw_text": "References & Team: Research papers on traffic Signal RL. Contact: team@example.com.",
            "word_count": 12,
            "bullet_count": 2,
            "image_count": 0
        }
    ]

    report = ScoreAggregator.process_submission(
        slides=sample_slides,
        ps_title="AI-Based Smart Traffic Management System for Urban Cities",
        ps_description="Develop an intelligent real-time traffic signal optimization system using computer vision and IoT sensors."
    )

    print("--- SCORING TEST RESULT ---")
    print(f"Overall Score: {report['overall_score']}/100")
    print(f"Verdict: {report['verdict_text']}")
    print("Breakdown:", report['category_breakdown'])

    assert report['overall_score'] >= 80, "Expected high score for well-formatted 6-slide deck"
    print("ALL UNIT TESTS PASSED CLEANLY!")

if __name__ == "__main__":
    test_scoring_pipeline()
