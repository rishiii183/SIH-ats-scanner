import math
import re
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
    # Lazy load or initialize lightweight local model
    _model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    _model = None


class PSAlignmentScorer:
    """
    Evaluates Problem Statement Alignment:
    Compares presentation slide text against the chosen official SIH Problem Statement.
    Uses sentence-transformers cosine similarity with fallback token overlap.
    """

    @classmethod
    def _cosine_similarity(cls, vec1: List[float], vec2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    @classmethod
    def _fallback_keyword_similarity(cls, text1: str, text2: str) -> float:
        words1 = set(re.findall(r'\b[a-zA-Z]{3,}\b', text1.lower()))
        words2 = set(re.findall(r'\b[a-zA-Z]{3,}\b', text2.lower()))
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)

    @classmethod
    def evaluate(
        cls, 
        slides: List[Dict[str, Any]], 
        ps_title: str, 
        ps_description: str
    ) -> Dict[str, Any]:
        
        full_deck_text = " ".join([slide["raw_text"] for slide in slides])
        ps_full_text = f"{ps_title}. {ps_description}"

        if not full_deck_text.strip():
            return {
                "score": 0.0,
                "reasons": [{"deduction": 100.0, "message": "No readable text found in submission.", "cited_source": None}],
                "similarity_score": 0.0
            }

        # Embed or fallback
        if _model is not None:
            try:
                embeddings = _model.encode([full_deck_text, ps_full_text])
                similarity = cls._cosine_similarity(embeddings[0].tolist(), embeddings[1].tolist())
            except Exception:
                similarity = cls._fallback_keyword_similarity(full_deck_text, ps_full_text)
        else:
            similarity = cls._fallback_keyword_similarity(full_deck_text, ps_full_text)

        # Scale similarity (typically 0.3 - 0.85 in sentence-transformers) to 0 - 100 score
        # Similarity >= 0.65 -> 90-100 score
        # Similarity 0.45 - 0.65 -> 70-90 score
        # Similarity < 0.45 -> <70 score
        if similarity >= 0.65:
            score = 95.0 + (similarity - 0.65) * 20.0
        elif similarity >= 0.45:
            score = 70.0 + (similarity - 0.45) * 125.0
        else:
            score = max(20.0, similarity * 155.0)

        score = min(100.0, max(0.0, score))
        reasons = []

        if similarity < 0.50:
            reasons.append({
                "deduction": round(100.0 - score, 1),
                "evidence": f"Calculated cosine similarity score is {round(similarity, 3)} against PS '{ps_title}'.",
                "rule_violated": "min_semantic_similarity_threshold: 0.50",
                "source_type": "rubric_citation",
                "message": f"Semantic analysis indicates moderate domain alignment with selected PS '{ps_title}' (Cosine Similarity: {round(similarity, 3)}). Ensure problem & solution slides explicitly echo core domain terms.",
                "cited_source": "SIH Evaluation Rubric §1: Solution alignment with specified problem statement."
            })
        else:
            reasons.append({
                "deduction": 0.0,
                "evidence": f"Calculated cosine similarity score is {round(similarity, 3)} against PS '{ps_title}'.",
                "rule_violated": "none (strong domain match)",
                "source_type": "rubric_citation",
                "message": f"Strong domain alignment verified with Problem Statement '{ps_title}' (Cosine Similarity: {round(similarity, 3)}).",
                "cited_source": "SIH Evaluation Rubric §1: Domain Alignment Pass."
            })

        return {
            "status": "available",
            "confidence_type": "estimated",
            "score": round(score, 1),
            "similarity_score": round(float(similarity), 3),
            "reasons": reasons
        }


