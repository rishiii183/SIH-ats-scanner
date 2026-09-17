import json
import re
import os
import requests
from typing import List, Dict, Any

class TechDepthScorer:
    """
    Evaluates Technical Depth & Implementation Feasibility using Google Gemini 1.5 Flash.
    Checks for:
    - Named specific technologies (e.g. FastAPI, PostgreSQL, TensorRT) vs generic terms ("Backend, Database")
    - Architecture & pipeline feasibility
    - Implementation roadmap clarity
    """

    @classmethod
    def evaluate(
        cls, 
        slides: List[Dict[str, Any]], 
        gemini_api_key: str = ""
    ) -> Dict[str, Any]:
        
        # Isolate technical slides (typically slides 3, 4, 5) or full deck text
        tech_slides_text = ""
        for slide in slides:
            text = slide["raw_text"]
            if any(kw in text.lower() for kw in ["tech", "architecture", "stack", "feasibility", "implementation", "solution", "database"]):
                tech_slides_text += f"\n--- Slide {slide['slide_number']} ---\n{text}"

        if not tech_slides_text:
            tech_slides_text = "\n".join([f"Slide {s['slide_number']}: {s['raw_text']}" for s in slides])

        api_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "")

        # Call Gemini if API Key is available
        if api_key:
            try:
                prompt = (
                    "You are a senior hackathon evaluator for Smart India Hackathon (SIH 2026).\n"
                    "Evaluate the technical depth, technology stack specificity, and implementation feasibility of the following presentation slides:\n\n"
                    f"{tech_slides_text}\n\n"
                    "Instructions:\n"
                    "1. Check if SPECIFIC technologies/frameworks are named (e.g. PyTorch, PostgreSQL, Docker, Redis) rather than vague words ('AI', 'Cloud', 'Database').\n"
                    "2. Check if technical workflow/architecture is clear.\n"
                    "3. Return ONLY a valid JSON object matching this schema:\n"
                    "{\n"
                    '  "score": <number 0 to 100>,\n'
                    '  "reason": "<1-2 sentence explainable reason for score>",\n'
                    '  "named_technologies": ["<tech1>", "<tech2>"],\n'
                    '  "rewrite_suggestion": "<1 concrete suggestion to improve technical depth score>"\n'
                    "}\n"
                )

                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
                }

                response = requests.post(url, headers=headers, json=payload, timeout=10)
                if response.status_code == 200:
                    resp_json = response.json()
                    content = resp_json['candidates'][0]['content']['parts'][0]['text']
                    result = json.loads(content)
                    
                    score = float(result.get("score", 75))
                    reason = result.get("reason", "Evaluated via Gemini 1.5 Flash AI.")
                    rewrite = result.get("rewrite_suggestion", "")

                    return {
                        "score": round(score, 1),
                        "reasons": [{
                            "deduction": round(100.0 - score, 1),
                            "message": reason,
                            "cited_source": "SIH Evaluation Rubric §2: Technical Approach & Feasibility."
                        }],
                        "rewrite_suggestion": rewrite,
                        "llm_used": True
                    }
            except Exception as e:
                # Log error and fall back smoothly
                pass

        # Rule-based fallback if LLM call is unavailable
        return cls._fallback_rule_based_evaluation(tech_slides_text)

    @classmethod
    def _fallback_rule_based_evaluation(cls, text: str) -> Dict[str, Any]:
        score = 70.0
        reasons = []

        # List of common specific technology terms
        tech_keywords = [
            "python", "react", "fastapi", "nodejs", "express", "postgresql", "mongodb", "redis",
            "docker", "kubernetes", "pytorch", "tensorflow", "opencv", "yolo", "aws", "gcp", "azure",
            "solidity", "flutter", "react native", "tensorrt", "scikit-learn", "langchain", "llama"
        ]

        text_lower = text.lower()
        found_techs = [tech for tech in tech_keywords if tech in text_lower]

        if len(found_techs) >= 4:
            score += 25.0
            reasons.append({
                "deduction": 0.0,
                "message": f"Strong technical specificity: Named concrete technologies ({', '.join(found_techs[:5])}).",
                "cited_source": "SIH Tech Depth Rubric: Specific Technology Stack Named."
            })
        elif len(found_techs) >= 2:
            score += 10.0
            reasons.append({
                "deduction": 15.0,
                "message": f"Moderate technical specificity ({', '.join(found_techs)}). Consider specifying exact databases, frameworks, and deployment stack.",
                "cited_source": "SIH Tech Depth Rubric: Technology Stack Explicit Choice."
            })
        else:
            score -= 20.0
            reasons.append({
                "deduction": 30.0,
                "message": "Generic technical descriptions detected. Replace buzzwords ('AI', 'Cloud', 'DB') with exact libraries, models, and frameworks.",
                "cited_source": "SIH Tech Depth Rubric: Penalty for Vague Technology References."
            })

        final_score = min(100.0, max(0.0, score))
        return {
            "score": round(final_score, 1),
            "reasons": reasons,
            "rewrite_suggestion": "Specify exact tech stack components (e.g. replace 'AI Model' with 'YOLOv8 fine-tuned on custom dataset' or 'PostgreSQL with pgvector').",
            "llm_used": False
        }
