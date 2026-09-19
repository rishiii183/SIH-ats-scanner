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

        if not api_key:
            return {
                "status": "not_available",
                "confidence_type": "estimated",
                "score": None,
                "reasons": [{
                    "deduction": 0.0,
                    "evidence": "No GEMINI_API_KEY environment variable configured.",
                    "rule_violated": "llm_api_key_required",
                    "source_type": "llm_reasoning",
                    "message": "Technical Depth AI evaluation requires a Gemini API key. Category skipped and weights renormalized across active evaluation pillars.",
                    "cited_source": "System Configuration: LLM API Key Required"
                }],
                "rewrite_suggestion": "AI slide rewrite generator is unavailable without an active LLM API key.",
                "llm_used": False
            }

        try:
            prompt = (
                "You are an expert technical auditor for Smart India Hackathon (SIH 2026).\n"
                "Audit the following presentation slide text for technical implementation depth.\n\n"
                f"{tech_slides_text}\n\n"
                "Instructions:\n"
                "Evaluate the 4 binary criteria below. Quoted evidence MUST be exact strings from the slide text.\n"
                "Return ONLY a valid JSON object with this exact schema:\n"
                "{\n"
                '  "names_specific_framework_or_language": {"present": true, "extracted_evidence": "Python, FastAPI"},\n'
                '  "names_specific_database_or_storage": {"present": true, "extracted_evidence": "PostgreSQL with pgvector"},\n'
                '  "names_specific_model_or_algorithm": {"present": true, "extracted_evidence": "YOLOv8 object detection"},\n'
                '  "describes_architecture_or_workflow": {"present": true, "extracted_evidence": "CCTV camera feeds processed at quad-intersections"},\n'
                '  "rewrite_suggestion": "<1 concrete actionable technical improvement>"\n'
                "}\n"
            )

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
            }

            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                resp_json = response.json()
                content = resp_json['candidates'][0]['content']['parts'][0]['text']
                checklist = json.loads(content)
                return cls._compute_score_from_checklist(checklist, llm_used=True)
        except Exception:
            pass

        # Fallback if Gemini call fails or times out
        return {
            "status": "not_available",
            "confidence_type": "estimated",
            "score": None,
            "reasons": [{
                "deduction": 0.0,
                "evidence": "Gemini API request exception or timeout.",
                "rule_violated": "llm_call_failed",
                "source_type": "llm_reasoning",
                "message": "Technical Depth AI evaluation call failed. Category skipped and weights renormalized.",
                "cited_source": "System Status: LLM Call Failed"
            }],
            "rewrite_suggestion": "AI slide rewrite generator is currently unavailable.",
            "llm_used": False
        }

    @classmethod
    def _compute_score_from_checklist(cls, checklist: Dict[str, Any], llm_used: bool = True) -> Dict[str, Any]:
        score = 50.0
        reasons = []
        evidence_list = []

        criteria_map = [
            ("names_specific_framework_or_language", "Specific Framework/Language Named (+12.5 pts)", "missing_specific_frameworks"),
            ("names_specific_database_or_storage", "Specific Database/Storage Named (+12.5 pts)", "missing_specific_database"),
            ("names_specific_model_or_algorithm", "Specific Model/Algorithm Named (+12.5 pts)", "missing_specific_models"),
            ("describes_architecture_or_workflow", "Concrete Architecture/Workflow Described (+12.5 pts)", "vague_architecture_description")
        ]

        for key, label, rule_code in criteria_map:
            item = checklist.get(key, {})
            present = item.get("present", False)
            ev = item.get("extracted_evidence", "None")
            
            if present:
                score += 12.5
                evidence_list.append(f"{label}: '{ev}'")
            else:
                reasons.append({
                    "deduction": 12.5,
                    "evidence": f"Audited criterion '{key}': not found in technical slides.",
                    "rule_violated": rule_code,
                    "source_type": "llm_reasoning",
                    "message": f"Technical depth checklist flag: {label.split(' (+')[0]} missing or vague.",
                    "cited_source": "SIH Technical Evaluation Criteria §2: Technology Specificity."
                })

        final_score = min(100.0, max(0.0, score))
        if not reasons:
            reasons.append({
                "deduction": 0.0,
                "evidence": " | ".join(evidence_list),
                "rule_violated": "none (all 4 criteria passed)",
                "source_type": "llm_reasoning",
                "message": "Strong technical specificity verified: named explicit frameworks, database, model, and architecture flow.",
                "cited_source": "SIH Technical Evaluation Criteria §2: Technical Depth Pass."
            })

        return {
            "status": "available",
            "confidence_type": "estimated",
            "score": round(final_score, 1),
            "raw_checklist": checklist,
            "reasons": reasons,
            "rewrite_suggestion": checklist.get("rewrite_suggestion", "Include specific databases and deep learning models in slide 4."),
            "llm_used": llm_used
        }

    @classmethod
    def _fallback_checklist_evaluation(cls, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # 1. Framework / Language
        fw_match = re.search(r'\b(fastapi|flask|express|react|next|vue|angular|django|spring|solidity|python|java|cpp|rust|go|node|esp32)\b', text_lower)
        fw_present = bool(fw_match)
        fw_ev = fw_match.group(0) if fw_match else ""

        # 2. Database / Storage
        db_match = re.search(r'\b(postgres|postgresql|mysql|mongodb|redis|sqlite|influxdb|ipfs|dynamodb|pgvector|database)\b', text_lower)
        db_present = bool(db_match)
        db_ev = db_match.group(0) if db_match else ""

        # 3. Model / Algorithm
        model_match = re.search(r'\b(yolov8|yolo|bert|resnet|transformer|random forest|xgboost|cnn|rnn|knn|svm|smart contract|deep learning|computer vision)\b', text_lower)
        model_present = bool(model_match)
        model_ev = model_match.group(0) if model_match else ""

        # 4. Architecture / Workflow
        arch_match = re.search(r'\b(architecture|workflow|pipeline|ingestion|telemetry|microcontroller|camera|sensor|edge|feed|traceability|node)\b', text_lower)
        arch_present = bool(arch_match)
        arch_ev = arch_match.group(0) if arch_match else ""

        return {
            "names_specific_framework_or_language": {"present": fw_present, "extracted_evidence": fw_ev},
            "names_specific_database_or_storage": {"present": db_present, "extracted_evidence": db_ev},
            "names_specific_model_or_algorithm": {"present": model_present, "extracted_evidence": model_ev},
            "describes_architecture_or_workflow": {"present": arch_present, "extracted_evidence": arch_ev},
            "rewrite_suggestion": "Specify exact database indexing (e.g. pgvector) and model inference latency targets."
        }



