from typing import List, Dict, Any
from app.scoring.structure import StructureScorer
from app.scoring.clarity import ClarityScorer
from app.scoring.ps_alignment import PSAlignmentScorer
from app.scoring.tech_depth import TechDepthScorer
from app.scoring.originality import OriginalityScorer

class ScoreAggregator:
    DEFAULT_WEIGHTS = {
        "structure_format": 0.15,
        "ps_alignment": 0.20,
        "technical_depth": 0.30,
        "originality": 0.20,
        "clarity": 0.15
    }

    @classmethod
    def process_submission(
        cls, 
        slides: List[Dict[str, Any]], 
        ps_title: str = "General Track", 
        ps_description: str = "",
        custom_weights: Dict[str, float] = None,
        gemini_api_key: str = ""
    ) -> Dict[str, Any]:
        
        weights = custom_weights or cls.DEFAULT_WEIGHTS

        # 1. Run Category Modules
        struct_res = StructureScorer.evaluate(slides)
        clarity_res = ClarityScorer.evaluate(slides)
        align_res = PSAlignmentScorer.evaluate(slides, ps_title, ps_description)
        tech_res = TechDepthScorer.evaluate(slides, gemini_api_key)
        orig_res = OriginalityScorer.evaluate(slides)

        # 2. Compute Weighted Score
        overall_score = (
            struct_res["score"] * weights.get("structure_format", 0.15) +
            align_res["score"] * weights.get("ps_alignment", 0.20) +
            tech_res["score"] * weights.get("technical_depth", 0.30) +
            orig_res["score"] * weights.get("originality", 0.20) +
            clarity_res["score"] * weights.get("clarity", 0.15)
        )

        overall_score = round(overall_score, 1)

        # 3. Determine Verdict Text
        if overall_score >= 85:
            verdict = "Strong candidate for national shortlisting. Meets SIH 2026 guidelines."
        elif overall_score >= 70:
            verdict = "Competitive deck. Fix highlighted technical depth & section flags to maximize score."
        elif overall_score >= 50:
            verdict = "Needs refinement before submission. Review slide count and section structure."
        else:
            verdict = "High risk of early elimination. Format or content significantly deviates from official rubric."

        # 4. Compile Rewrite Suggestions
        rewrite_suggestions = []
        if tech_res.get("rewrite_suggestion"):
            rewrite_suggestions.append({
                "category": "Technical Depth",
                "suggestion": tech_res["rewrite_suggestion"]
            })
        if struct_res.get("missing_sections"):
            rewrite_suggestions.append({
                "category": "Structure & Format",
                "suggestion": f"Add explicit slide titles for missing mandatory sections: {', '.join(struct_res['missing_sections'])}."
            })
        if clarity_res.get("avg_words_per_slide", 0) > 80:
            rewrite_suggestions.append({
                "category": "Presentation Clarity",
                "suggestion": "Convert paragraph descriptions into bullet points and system flow diagrams."
            })

        return {
            "overall_score": overall_score,
            "verdict_text": verdict,
            "rubric_stamp": "Scored against official SIH 2026 IDEA Presentation Format",
            "category_breakdown": {
                "structure_format": {
                    "score": struct_res["score"],
                    "weight": weights.get("structure_format", 0.15),
                    "reasons": struct_res["reasons"]
                },
                "ps_alignment": {
                    "score": align_res["score"],
                    "weight": weights.get("ps_alignment", 0.20),
                    "reasons": align_res["reasons"],
                    "similarity": align_res.get("similarity_score", 0)
                },
                "technical_depth": {
                    "score": tech_res["score"],
                    "weight": weights.get("technical_depth", 0.30),
                    "reasons": tech_res["reasons"]
                },
                "originality": {
                    "score": orig_res["score"],
                    "weight": weights.get("originality", 0.20),
                    "reasons": orig_res["reasons"]
                },
                "clarity": {
                    "score": clarity_res["score"],
                    "weight": weights.get("clarity", 0.15),
                    "reasons": clarity_res["reasons"]
                }
            },
            "rewrite_suggestions": rewrite_suggestions
        }
