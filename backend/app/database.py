import os
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from supabase import create_client, Client
from app.config import settings

# Initialize Supabase Python Client
try:
    supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
except Exception as e:
    print(f"Warning: Failed to initialize Supabase client: {e}")
    supabase_client = None

# In-Memory Fallback & Progress Cache
PROGRESS_CACHE: Dict[str, Dict[str, Any]] = {}

class DBManager:
    """
    Production Database & Storage Manager for SIH ATS Scanner.
    Powered by Supabase PostgreSQL and Supabase Storage.
    """

    @classmethod
    def get_client(cls) -> Optional[Client]:
        return supabase_client

    # ==========================================
    # 1. CLOUD STORAGE (SUPABASE BUCKET)
    # ==========================================
    @classmethod
    def upload_file_to_storage(cls, file_bytes: bytes, filename: str) -> str:
        """
        Uploads presentation file directly to Supabase Storage Bucket ('sih-decks').
        Returns public URL or accessible reference URL.
        """
        client = cls.get_client()
        unique_name = f"{uuid.uuid4()}_{filename}"
        
        if client:
            try:
                content_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation" if filename.endswith(".pptx") else "application/pdf"
                
                # Upload to Supabase Storage
                client.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=unique_name,
                    file=file_bytes,
                    file_options={"content-type": content_type}
                )

                # Get public URL
                res = client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(unique_name)
                return res
            except Exception as e:
                print(f"Supabase Storage Upload Warning: {e}")
                return f"local://{filename}"
        return f"local://{filename}"

    # ==========================================
    # 2. RUBRIC CONFIGS & CORPUS
    # ==========================================
    @classmethod
    def get_active_rubric_config(cls, year: int = 2026) -> Dict[str, Any]:
        """
        Reads active rubric configuration directly from Supabase 'rubric_configs' table.
        """
        client = cls.get_client()
        if client:
            try:
                res = client.table("rubric_configs").select("*").eq("year", year).eq("status", "active").limit(1).execute()
                if res.data and len(res.data) > 0:
                    return res.data[0]
            except Exception as e:
                print(f"Supabase fetch rubric_configs error: {e}")

        # Fallback baseline configuration for SIH 2026
        return {
            "id": "cdbb77e8-ee1c-41bc-b780-af3395c5f706",
            "year": 2026,
            "status": "active",
            "max_slides": 6,
            "allowed_file_types": ["pdf", "pptx"],
            "max_file_size_mb": 25,
            "required_sections": [
                {"name": "Title Slide", "keywords": ["title", "team", "ps", "problem statement", "theme"]},
                {"name": "Problem Statement", "keywords": ["problem", "challenge", "background", "need", "issue"]},
                {"name": "Proposed Solution", "keywords": ["solution", "approach", "idea", "innovation", "proposed"]},
                {"name": "Technical Approach", "keywords": ["tech stack", "architecture", "technology", "feasibility", "implementation", "methodology"]},
                {"name": "Impact & Benefits", "keywords": ["impact", "benefits", "scalability", "outcomes", "social", "economic"]},
                {"name": "References & Team", "keywords": ["references", "team", "members", "contact", "mentor"]}
            ],
            "category_weights": {
                "structure_format": 0.15,
                "ps_alignment": 0.20,
                "technical_depth": 0.30,
                "originality": 0.20,
                "clarity": 0.15
            },
            "source_doc_text": "Official SIH 2026 Idea Presentation Format: Maximum 6 slides."
        }

    @classmethod
    def get_corpus_count(cls) -> int:
        """
        Checks row count of 'corpus_documents' table in Supabase.
        """
        client = cls.get_client()
        if client:
            try:
                res = client.table("corpus_documents").select("count", count="exact").execute()
                return res.count or 0
            except Exception:
                return 0
        return 0

    # ==========================================
    # 3. PROBLEM STATEMENTS
    # ==========================================
    @classmethod
    def get_problem_statements(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        client = cls.get_client()
        if client:
            try:
                req = client.table("problem_statements").select("id, ps_id, title, description, theme, category")
                if query:
                    q = query.strip()
                    req = req.or_(f"title.ilike.%{q}%,ps_id.ilike.%{q}%,theme.ilike.%{q}%")
                
                res = req.order("ps_id", desc=False).execute()
                if res.data:
                    return res.data
            except Exception as e:
                print(f"Supabase fetch problem statements error: {e}")
        
        # Fallback problem bank
        return [
            {"id": "SIH26101", "ps_id": "SIH26101", "title": "AI-Based Smart Traffic Management System for Urban Cities", "theme": "Smart Cities", "category": "software"},
            {"id": "SIH26102", "ps_id": "SIH26102", "title": "Automated Resume and Presentation ATS Evaluator", "theme": "EdTech", "category": "software"},
            {"id": "SIH26103", "ps_id": "SIH26103", "title": "Blockchain-Based Supply Chain Transparency for Agriculture Products", "theme": "AgriTech", "category": "software"},
            {"id": "SIH26104", "ps_id": "SIH26104", "title": "IoT-Enabled Water Leakage and Quality Monitoring Network", "theme": "Clean & Green Tech", "category": "hardware"},
            {"id": "SIH26105", "ps_id": "SIH26105", "title": "Early Detection of Crop Diseases Using Satellite and Drone Imagery", "theme": "AgriTech", "category": "software"}
        ]

    @classmethod
    def get_problem_statement_by_id(cls, ps_id: str) -> Optional[Dict[str, Any]]:
        client = cls.get_client()
        if client and ps_id:
            try:
                res = client.table("problem_statements").select("*").or_(f"id.eq.{ps_id},ps_id.eq.{ps_id}").limit(1).execute()
                if res.data and len(res.data) > 0:
                    return res.data[0]
            except Exception as e:
                print(f"Supabase get PS error: {e}")

        # Fallback lookup
        for ps in cls.get_problem_statements():
            if ps["id"] == ps_id or ps["ps_id"].lower() == ps_id.lower():
                return ps
        return None

    # ==========================================
    # 3. SUBMISSIONS
    # ==========================================
    @classmethod
    def create_submission(
        cls, 
        file_name: str, 
        file_type: str, 
        file_url: str = "local", 
        ps_id: Optional[str] = None,
        user_email: Optional[str] = None
    ) -> Dict[str, Any]:
        sub_id = str(uuid.uuid4())
        client = cls.get_client()
        user_id = None

        if client and user_email:
            try:
                user_res = client.table("users").select("id").eq("email", user_email.lower().trim()).maybe_single().execute()
                if user_res.data:
                    user_id = user_res.data["id"]
            except Exception:
                pass

        record = {
            "id": sub_id,
            "file_name": file_name,
            "file_type": file_type,
            "file_url": file_url,
            "status": "queued",
            "progress_step": "Queued for evaluation...",
            "progress_pct": 10,
            "created_at": datetime.now().isoformat()
        }

        # Store in Supabase PostgreSQL
        if client:
            try:
                db_payload: Dict[str, Any] = {
                    "id": sub_id,
                    "file_name": file_name,
                    "file_type": file_type,
                    "file_url": file_url,
                    "status": "queued"
                }
                if user_id:
                    db_payload["user_id"] = user_id
                
                client.table("submissions").insert(db_payload).execute()
            except Exception as e:
                print(f"Supabase create submission error: {e}")

        # Update local progress cache
        PROGRESS_CACHE[sub_id] = record
        return record

    @classmethod
    def update_submission_status(
        cls, 
        sub_id: str, 
        status: str, 
        step: str, 
        pct: int, 
        error_message: Optional[str] = None
    ):
        if sub_id not in PROGRESS_CACHE:
            PROGRESS_CACHE[sub_id] = {"id": sub_id}

        PROGRESS_CACHE[sub_id]["status"] = status
        PROGRESS_CACHE[sub_id]["progress_step"] = step
        PROGRESS_CACHE[sub_id]["progress_pct"] = pct
        if error_message:
            PROGRESS_CACHE[sub_id]["error_message"] = error_message

        client = cls.get_client()
        if client:
            try:
                update_payload = {"status": status}
                if error_message:
                    update_payload["error_message"] = error_message
                client.table("submissions").update(update_payload).eq("id", sub_id).execute()
            except Exception as e:
                print(f"Supabase update status error: {e}")

    @classmethod
    def get_submission(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        # Check cache for fast real-time progress polling
        if sub_id in PROGRESS_CACHE:
            return PROGRESS_CACHE[sub_id]

        client = cls.get_client()
        if client:
            try:
                res = client.table("submissions").select("*").eq("id", sub_id).maybe_single().execute()
                if res.data:
                    return res.data
            except Exception as e:
                print(f"Supabase get submission error: {e}")

        return None

    # ==========================================
    # 4. REPORTS & SCORES
    # ==========================================
    @classmethod
    def save_report(cls, sub_id: str, report_data: Dict[str, Any]):
        # Update progress cache
        PROGRESS_CACHE[sub_id] = {
            "id": sub_id,
            "status": "completed",
            "progress_step": "Report finalized",
            "progress_pct": 100,
            "report": report_data
        }

        cls.update_submission_status(sub_id, "completed", "Report finalized", 100)

        client = cls.get_client()
        if client:
            try:
                # 1. Save main report row
                report_payload = {
                    "submission_id": sub_id,
                    "overall_score": report_data.get("overall_score", 0),
                    "verdict_text": report_data.get("verdict_text", "Evaluation Complete"),
                    "category_breakdown": report_data.get("category_breakdown", {}),
                    "rewrite_suggestions": report_data.get("rewrite_suggestions", [])
                }
                client.table("reports").upsert(report_payload, on_conflict="submission_id").execute()

                # 2. Save individual category scores (only for active available categories)
                breakdown = report_data.get("category_breakdown", {})
                for cat_key, cat_val in breakdown.items():
                    if cat_val.get("status") == "available" and cat_val.get("score") is not None:
                        score_payload = {
                            "submission_id": sub_id,
                            "category": cat_key,
                            "raw_score": cat_val.get("score", 0),
                            "weight_applied": cat_val.get("weight_applied", cat_val.get("weight", 0.2)),
                            "reasons": cat_val.get("reasons", [])
                        }
                        client.table("scores").insert(score_payload).execute()

            except Exception as e:
                print(f"Supabase save report & scores error: {e}")

    @classmethod
    def get_report(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        # Fast cache hit
        if sub_id in PROGRESS_CACHE and "report" in PROGRESS_CACHE[sub_id]:
            return PROGRESS_CACHE[sub_id]["report"]

        client = cls.get_client()
        if client:
            try:
                res = client.table("reports").select("*").eq("submission_id", sub_id).maybe_single().execute()
                if res.data:
                    return {
                        "overall_score": float(res.data.get("overall_score", 0)),
                        "verdict_text": res.data.get("verdict_text", ""),
                        "rubric_stamp": "Scored against official SIH 2026 IDEA Presentation Format",
                        "category_breakdown": res.data.get("category_breakdown", {}),
                        "rewrite_suggestions": res.data.get("rewrite_suggestions", [])
                    }
            except Exception as e:
                print(f"Supabase fetch report error: {e}")

        return None
