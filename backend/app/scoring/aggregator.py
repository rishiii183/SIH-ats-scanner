from typing import List, Dict, Any, Optional
from app.database import DBManager
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
        gemini_api_key: str = "",
        rubric_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        # Load active rubric config if not passed explicitly
        if not rubric_config:
            rubric_config = DBManager.get_active_rubric_config()

        rubric_config_id = rubric_config.get("id", "sih-2026-default")
        nominal_weights = custom_weights or rubric_config.get("category_weights", cls.DEFAULT_WEIGHTS)
        corpus_count = DBManager.get_corpus_count()

        # 1. Run Category Modules
        struct_res = StructureScorer.evaluate(slides, rubric_config)
        clarity_res = ClarityScorer.evaluate(slides)
        align_res = PSAlignmentScorer.evaluate(slides, ps_title, ps_description)
        tech_res = TechDepthScorer.evaluate(slides, gemini_api_key)
        orig_res = OriginalityScorer.evaluate(slides, corpus_count)

        raw_results = {
            "structure_format": struct_res,
            "ps_alignment": align_res,
            "technical_depth": tech_res,
            "originality": orig_res,
            "clarity": clarity_res
        }

        # 2. Dynamic Weight Renormalization for Active Categories
        active_weights = {}
        total_active_weight = 0.0
        missing_weight = 0.0
        missing_categories = []

        for cat_key, res in raw_results.items():
            nom_w = nominal_weights.get(cat_key, 0.20)
            if res.get("status") == "available" and res.get("score") is not None:
                active_weights[cat_key] = nom_w
                total_active_weight += nom_w
            else:
                active_weights[cat_key] = 0.0
                missing_weight += nom_w
                missing_categories.append(cat_key)

        renormalized_weights = {}
        overall_score = 0.0

        if total_active_weight > 0:
            for cat_key, nom_w in active_weights.items():
                if nom_w > 0:
                    r_w = nom_w / total_active_weight
                    renormalized_weights[cat_key] = round(r_w, 4)
                    overall_score += raw_results[cat_key]["score"] * r_w
                else:
                    renormalized_weights[cat_key] = 0.0
        else:
            overall_score = 0.0

        overall_score = round(overall_score, 1)
        missing_weight = round(missing_weight, 4)
        evaluation_completeness = "full" if missing_weight == 0.0 else "partial"

        # 3. Determine Verdict Text with Partial Evaluation Protection
        missing_cat_names = [c.replace('_', ' ').title() for c in missing_categories]
        
        if missing_weight >= 0.30:
            # Prevent false shortlisting claims when 30%+ of rubric pillars were unassessed
            if overall_score >= 70:
                verdict = (
                    f"Partial evaluation ({round((1.0 - missing_weight) * 100)}% of rubric scored). "
                    f"Structure, Clarity, and PS Alignment look strong, but {', '.join(missing_cat_names)} "
                    f"could not be assessed due to unconfigured API/empty corpus. THIS IS NOT A COMPLETE SCORE."
                )
            else:
                verdict = (
                    f"Partial evaluation ({round((1.0 - missing_weight) * 100)}% of rubric scored). "
                    f"Deck has structural/alignment flags, and {', '.join(missing_cat_names)} "
                    f"could not be assessed. THIS IS NOT A COMPLETE SCORE."
                )
        else:
            if overall_score >= 85:
                verdict = "Strong candidate for national shortlisting. Meets SIH guidelines across assessed pillars."
            elif overall_score >= 70:
                verdict = "Competitive deck. Fix highlighted section/clarity flags to maximize score."
            elif overall_score >= 50:
                verdict = "Needs refinement before submission. Review slide count and section structure."
            else:
                verdict = "High risk of early elimination. Format or content significantly deviates from rubric."

        # 4. Compile Rewrite Suggestions
        rewrite_suggestions = []
        if tech_res.get("status") == "available" and tech_res.get("rewrite_suggestion"):
            rewrite_suggestions.append({
                "category": "Technical Depth",
                "suggestion": tech_res["rewrite_suggestion"]
            })
        elif tech_res.get("status") == "not_available":
            rewrite_suggestions.append({
                "category": "Technical Depth AI",
                "suggestion": "Configure Gemini API key to enable AI-powered technical depth suggestions."
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

        # 5. Build Category Breakdown with confidence_type and explicit phrasing
        category_breakdown = {}
        confidence_type_map = {
            "structure_format": "hard_check",
            "clarity": "hard_check",
            "ps_alignment": "estimated",
            "technical_depth": "estimated",
            "originality": "estimated"
        }

        for cat_key, res in raw_results.items():
            conf_type = confidence_type_map.get(cat_key, "estimated")
            category_breakdown[cat_key] = {
                "status": res.get("status", "available"),
                "confidence_type": conf_type,
                "score": res.get("score"),
                "nominal_weight": nominal_weights.get(cat_key, 0.20),
                "weight_applied": renormalized_weights.get(cat_key, 0.0),
                "reasons": res.get("reasons", [])
            }

        # Weight Math Details for Audit Trail
        math_steps = []
        for cat_key, nom_w in nominal_weights.items():
            res = raw_results.get(cat_key, {})
            status = res.get("status", "not_available")
            score_val = res.get("score")
            applied_w = renormalized_weights.get(cat_key, 0.0)
            if status == "available" and score_val is not None:
                math_steps.append(f"{cat_key}: {score_val} * {applied_w} = {round(score_val * applied_w, 3)}")
            else:
                math_steps.append(f"{cat_key}: NOT AVAILABLE (nominal weight {nom_w} redistributed)")

        weight_math_details = {
            "nominal_weights": nominal_weights,
            "total_active_weight": round(total_active_weight, 4),
            "missing_weight": missing_weight,
            "renormalized_weights": renormalized_weights,
            "calculation_formula": " + ".join([s for s in math_steps if "NOT AVAILABLE" not in s]),
            "overall_score": overall_score
        }

        disclaimer = (
            "DISCLAIMER: Scores reflect format compliance and content signals correlated with publicly "
            "available SIH criteria, not a guarantee of judging outcomes or shortlisting probability."
        )

        return {
            "overall_score": overall_score,
            "evaluation_completeness": evaluation_completeness,
            "missing_weight_pct": round(missing_weight * 100, 1),
            "missing_categories": missing_cat_names,
            "verdict_text": verdict,
            "disclaimer": disclaimer,
            "rubric_config_id": rubric_config_id,
            "rubric_stamp": f"Scored against Rubric Config ID #{rubric_config_id}",
            "active_pillars_count": len([w for w in renormalized_weights.values() if w > 0]),
            "category_breakdown": category_breakdown,
            "weight_math_details": weight_math_details,
            "rewrite_suggestions": rewrite_suggestions
        }


