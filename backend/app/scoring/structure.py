from typing import List, Dict, Any, Optional

class StructureScorer:
    """
    Evaluates Structure & Format Compliance against official SIH constraints.
    Reads rubric rules (max slides, required section lists) dynamically from rubric_configs data.
    """
    DEFAULT_REQUIRED_SECTIONS = [
        {"name": "Title Slide", "keywords": ["title", "team", "ps", "problem statement", "theme"]},
        {"name": "Problem Statement", "keywords": ["problem", "challenge", "background", "need", "issue"]},
        {"name": "Proposed Solution", "keywords": ["solution", "approach", "idea", "innovation", "proposed"]},
        {"name": "Technical Approach", "keywords": ["tech stack", "architecture", "technology", "feasibility", "implementation", "methodology"]},
        {"name": "Impact & Benefits", "keywords": ["impact", "benefits", "scalability", "outcomes", "social", "economic"]},
        {"name": "References & Team", "keywords": ["references", "team", "members", "contact", "mentor"]}
    ]

    @classmethod
    def evaluate(cls, slides: List[Dict[str, Any]], rubric_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        config = rubric_config or {}
        max_slides = config.get("max_slides", 6)
        required_sections = config.get("required_sections", cls.DEFAULT_REQUIRED_SECTIONS)
        rubric_config_id = config.get("id", "fallback-default-2026")

        score = 100.0
        reasons = []
        total_slides = len(slides)

        # 1. Slide Count Check (dynamic limit from rubric_config)
        if total_slides > max_slides:
            penalty = (total_slides - max_slides) * 15.0
            score -= penalty
            reasons.append({
                "deduction": round(penalty, 1),
                "message": f"Presentation has {total_slides} slides, exceeding the active rubric maximum limit of {max_slides} slides.",
                "cited_source": f"Rubric Config #{rubric_config_id}: Maximum slide count strictly capped at {max_slides} slides."
            })
        elif total_slides < 3:
            score -= 30.0
            reasons.append({
                "deduction": 30.0,
                "message": f"Presentation has only {total_slides} slides. Minimum expected is 3 slides to cover required sections.",
                "cited_source": f"Rubric Config #{rubric_config_id}: Insufficient slides to cover required proposal details."
            })

        # 2. Required Section Coverage Check
        full_text = " ".join([slide["raw_text"].lower() for slide in slides])
        missing_sections = []

        for section in required_sections:
            found = any(kw in full_text for kw in section.get("keywords", []))
            if not found:
                missing_sections.append(section.get("name", "Unknown Section"))

        if missing_sections:
            sec_penalty = len(missing_sections) * 10.0
            score -= sec_penalty
            reasons.append({
                "deduction": round(sec_penalty, 1),
                "message": f"Missing mandatory section headings: {', '.join(missing_sections)}.",
                "cited_source": f"Rubric Config #{rubric_config_id}: Decks must explicitly cover specified section topics."
            })

        final_score = max(0.0, min(100.0, score))
        if not reasons:
            reasons.append({
                "deduction": 0.0,
                "message": f"Deck perfectly satisfies the {max_slides}-slide count and required section structure guidelines.",
                "cited_source": f"Rubric Config #{rubric_config_id}: Structure Compliance Pass."
            })

        return {
            "status": "available",
            "score": round(final_score, 1),
            "reasons": reasons,
            "total_slides": total_slides,
            "missing_sections": missing_sections,
            "rubric_config_id": rubric_config_id
        }

