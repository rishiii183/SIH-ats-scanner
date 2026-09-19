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

        # Return graceful unavailable status if no API key is provided
        if not api_key:
            return {
                "status": "not_available",
                "score": None,
                "reasons": [{
                    "deduction": 0.0,
                    "message": "Technical Depth AI evaluation requires a Gemini API key. Category skipped and weights renormalized across active evaluation pillars.",
                    "cited_source": "System Configuration: LLM API Key Required"
                }],
                "rewrite_suggestion": "AI slide rewrite generator is unavailable without an active LLM API key.",
                "llm_used": False
            }

        # Call Gemini if API Key is available
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
                    "status": "available",
                    "score": round(score, 1),
                    "reasons": [{
                        "deduction": round(100.0 - score, 1),
                        "message": reason,
                        "cited_source": "SIH Evaluation Rubric §2: Technical Approach & Feasibility."
                    }],
                    "rewrite_suggestion": rewrite,
                    "llm_used": True
                }
        except Exception:
            pass

        return {
            "status": "not_available",
            "score": None,
            "reasons": [{
                "deduction": 0.0,
                "message": "Technical Depth AI evaluation call failed or timed out. Category skipped and weights renormalized.",
                "cited_source": "System Status: LLM Call Failed"
            }],
            "rewrite_suggestion": "AI slide rewrite generator is currently unavailable.",
            "llm_used": False
        }

