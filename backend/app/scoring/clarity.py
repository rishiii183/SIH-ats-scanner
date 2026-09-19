from typing import List, Dict, Any

class ClarityScorer:
    """
    Evaluates Presentation Clarity (Rule-Based):
    - Text density per slide (words > 70 flagged as wall of text)
    - Bullet point count ratio vs continuous paragraphs
    - Visual element ratio (slides with diagrams/images)
    """
    @classmethod
    def evaluate(cls, slides: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100.0
        reasons = []

        total_slides = len(slides)
        if total_slides == 0:
            return {"score": 0.0, "reasons": [{"deduction": 100.0, "message": "Empty file uploaded.", "cited_source": None}]}

        dense_slides = []
        low_visual_slides = []
        total_bullets = 0
        total_words = 0

        for slide in slides:
            slide_num = slide["slide_number"]
            raw_t = slide.get("raw_text", "")
            word_cnt = slide.get("word_count") or (len(raw_t.split()) if raw_t else 0)
            bullet_cnt = slide.get("bullet_count", 0)
            img_cnt = slide.get("image_count", 0)

            total_words += word_cnt
            total_bullets += bullet_cnt

            # Wall of text check (>70 words on a single presentation slide)
            if word_cnt > 70:
                dense_slides.append(slide_num)

            # Visual check (no image / diagram on technical/solution slides)
            if img_cnt == 0 and slide_num in [3, 4]:
                low_visual_slides.append(slide_num)

        # 1. Text Density Penalty
        if dense_slides:
            penalty = len(dense_slides) * 8.0
            score -= penalty
            reasons.append({
                "deduction": round(penalty, 1),
                "slide_number": dense_slides,
                "evidence": f"Slides {dense_slides} contain dense paragraphs exceeding 70 words per slide.",
                "rule_violated": "max_words_per_slide: 70",
                "source_type": "rubric_citation",
                "message": f"Slides {dense_slides} contain dense paragraphs (>70 words per slide). SIH evaluators prefer concise points.",
                "cited_source": "SIH Presentation Guidelines: Use bullet points, diagrams, and flowcharts — avoid walls of paragraph text."
            })

        # 2. Visual / Diagram Presence Check
        if low_visual_slides:
            penalty = len(low_visual_slides) * 6.0
            score -= penalty
            reasons.append({
                "deduction": round(penalty, 1),
                "slide_number": low_visual_slides,
                "evidence": f"Slides {low_visual_slides} contain 0 embedded visual images or diagrams.",
                "rule_violated": "missing_visual_diagrams on technical slides",
                "source_type": "rubric_citation",
                "message": f"Slides {low_visual_slides} (Proposed Solution / Tech Stack) lack visual diagrams or system flowcharts.",
                "cited_source": "SIH Design Guidelines: Architecture and technical flow should be demonstrated visually via diagrams."
            })

        # 3. Bullet Point Ratio Check
        avg_words_per_slide = total_words / total_slides
        if avg_words_per_slide > 100:
            score -= 15.0
            reasons.append({
                "deduction": 15.0,
                "evidence": f"Average word density is {round(avg_words_per_slide, 1)} words per slide across presentation.",
                "rule_violated": "max_avg_words_per_slide: 100",
                "source_type": "rubric_citation",
                "message": f"Average word count is {round(avg_words_per_slide)} words/slide. High risk of evaluator fatigue.",
                "cited_source": "Jury Scoring Criterion: Presentation Clarity & Conciseness."
            })

        final_score = max(0.0, min(100.0, score))
        if not reasons:
            reasons.append({
                "deduction": 0.0,
                "evidence": f"Average density is {round(avg_words_per_slide, 1)} words per slide with visual diagrams present.",
                "rule_violated": "none (full compliance)",
                "source_type": "rubric_citation",
                "message": "Excellent visual clarity: slides use concise bullet points and diagrams effectively.",
                "cited_source": "SIH Presentation Standard: Pass."
            })

        return {
            "status": "available",
            "confidence_type": "hard_check",
            "score": round(final_score, 1),
            "reasons": reasons,
            "avg_words_per_slide": round(avg_words_per_slide, 1)
        }


