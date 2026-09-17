import os
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

# In-Memory DB Store for fast local development and instant testing
IN_MEMORY_DB = {
    "problem_statements": [
        {
            "id": "ps-101",
            "ps_id": "SIH26101",
            "title": "AI-Based Smart Traffic Management System for Urban Cities",
            "description": "Develop an intelligent real-time traffic signal optimization system using computer vision and IoT sensors to reduce congestion at urban intersections and prioritize emergency vehicles.",
            "theme": "Smart Cities",
            "category": "software"
        },
        {
            "id": "ps-102",
            "ps_id": "SIH26102",
            "title": "Automated Resume and Presentation ATS Evaluator for Educational Institutions",
            "description": "Build an AI tool that evaluates student technical presentations and resumes against standard rubrics, providing line-by-line feedback and actionable improvement recommendations.",
            "theme": "EdTech",
            "category": "software"
        },
        {
            "id": "ps-103",
            "ps_id": "SIH26103",
            "title": "Blockchain-Based Supply Chain Transparency for Agriculture Products",
            "description": "Design a decentralized ledger system enabling farmers to track produce from harvest to consumer, ensuring fair pricing and authentic organic certification.",
            "theme": "AgriTech",
            "category": "software"
        },
        {
            "id": "ps-104",
            "ps_id": "SIH26104",
            "title": "IoT-Enabled Water Leakage and Quality Monitoring Network",
            "description": "Create a low-cost IoT sensor network for municipal water supply lines that detects chemical contaminants and flow leakages in real-time.",
            "theme": "Clean & Green Tech",
            "category": "hardware"
        },
        {
            "id": "ps-105",
            "ps_id": "SIH26105",
            "title": "Early Detection of Crop Diseases Using Satellite and Drone Imagery",
            "description": "Develop a computer vision platform that analyzes drone and multispectral satellite imagery to detect early crop pest infestations and nutrient deficiencies.",
            "theme": "AgriTech",
            "category": "software"
        }
    ],
    "submissions": {},
    "reports": {}
}

class DBManager:
    @classmethod
    def get_problem_statements(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        ps_list = IN_MEMORY_DB["problem_statements"]
        if query:
            q = query.lower()
            return [
                ps for ps in ps_list 
                if q in ps["ps_id"].lower() or q in ps["title"].lower() or q in ps["theme"].lower()
            ]
        return ps_list

    @classmethod
    def get_problem_statement_by_id(cls, ps_id: str) -> Optional[Dict[str, Any]]:
        for ps in IN_MEMORY_DB["problem_statements"]:
            if ps["id"] == ps_id or ps["ps_id"].lower() == ps_id.lower():
                return ps
        return None

    @classmethod
    def create_submission(cls, file_name: str, file_type: str, ps_id: Optional[str]) -> Dict[str, Any]:
        sub_id = str(uuid.uuid4())
        record = {
            "id": sub_id,
            "file_name": file_name,
            "file_type": file_type,
            "ps_id": ps_id,
            "status": "queued",
            "progress_step": "Queued for parsing...",
            "progress_pct": 10,
            "created_at": datetime.now().isoformat()
        }
        IN_MEMORY_DB["submissions"][sub_id] = record
        return record

    @classmethod
    def update_submission_status(cls, sub_id: str, status: str, step: str, pct: int):
        if sub_id in IN_MEMORY_DB["submissions"]:
            IN_MEMORY_DB["submissions"][sub_id]["status"] = status
            IN_MEMORY_DB["submissions"][sub_id]["progress_step"] = step
            IN_MEMORY_DB["submissions"][sub_id]["progress_pct"] = pct

    @classmethod
    def save_report(cls, sub_id: str, report_data: Dict[str, Any]):
        IN_MEMORY_DB["reports"][sub_id] = report_data
        cls.update_submission_status(sub_id, "completed", "Report finalized", 100)

    @classmethod
    def get_submission(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        return IN_MEMORY_DB["submissions"].get(sub_id)

    @classmethod
    def get_report(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        return IN_MEMORY_DB["reports"].get(sub_id)
