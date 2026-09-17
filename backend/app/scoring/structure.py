from typing import List, Dict, Any

class StructureScorer:
    """
    Evaluates Structure & Format Compliance against official SIH constraints.
    Max slides = 6. Checks for presence of 6 required content sections.
    """
    REQUIRED_SECTIONS = [
        {"name": "Title Slide", "keywords": ["title", "team", "ps", "problem statement", "theme"]},
        {"name": "Problem Statement", "keywords": ["problem", "challenge", "background", "need", "issue"]},
        {"name": "Proposed Solution", "keywords": ["solution", "approach", "idea", "innovation", "proposed"]},
        {"name": "Technical Approach", "keywords": ["tech stack", "architecture", "technology", "feasibility", "implementation", "methodology"]},
        {"name": "Impact & Benefits", "keywords": ["impact", "benefits", "scalability", "outcomes", "social", "economic"]},
        {"name": "References & Team", "keywords": ["references", "team", "members", "contact", "mentor"]}
    ]

    @classmethod
    def evaluate(cls, slides: List[Dict[str, Any]], max_slides: int = 6) -> Dict[str, Any]:
        score = 100.0
        reasons = []

        total_slides = len(slides)

        # 1. Slide Count Check (hard limit 6)
        if total_slides > max_slides:
            penalty = (total_slides - max_slides) * 15.0
            score -= penalty
            reasons.append({
                "deduction": round(penalty, 1),
                "message": f"Presentation has {total_slides} slides, exceeding the official SIH maximum limit of {max_slides} slides.",
                "cited_source": f"SIH 2026 Format Guidelines §1: Maximum slide count is strictly capped at {max_slides} slides."
            })
        elif total_slides < 3:
            score -= 30.0
            reasons.append({
                "deduction": 30.0,
                "message": f"Presentation has only {total_slides} slides. Recommended minimum is 4-6 slides to cover required sections.",
                "cited_source": "SIH 2026 Format Guidelines: Insufficient slides to cover required idea proposal details."
            })

        # 2. Required Section Coverage Check
        full_text = " ".join([slide["raw_text"].lower() for slide in slides])
        missing_sections = []

        for section in cls.REQUIRED_SECTIONS:
            found = any(kw in full_text for kw in section["keywords"])
            if not found:
                missing_sections.append(section["name"])

        if missing_sections:
            sec_penalty = len(missing_sections) * 10.0
            score -= sec_penalty
            reasons.append({
                "deduction": round(sec_penalty, 1),
                "message": f"Missing mandatory section headings: {', '.join(missing_sections)}.",
                "cited_source": "SIH 2026 Guidelines §2: Decks must explicitly cover Problem Statement, Solution, Tech Stack, Impact, and References."
            })

        final_score = max(0.0, min(100.0, score))
        if not reasons:
            reasons.append({
                "deduction": 0.0,
                "message": "Deck perfectly satisfies the 6-slide count and required section structure guidelines.",
                "cited_source": "SIH 2026 Official Rubric: Structure Compliance Pass."
            })

        return {
            "score": round(final_score, 1),
            "reasons": reasons,
            "total_slides": total_slides,
            "missing_sections": missing_sections
        }
