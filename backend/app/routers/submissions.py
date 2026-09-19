import os
from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, BackgroundTasks
from typing import Optional
from app.config import settings
from app.database import DBManager
from app.security import validate_uploaded_file, extract_user_from_auth_header, sanitize_text
from app.parsers.pptx_parser import PPTXParser
from app.parsers.pdf_parser import PDFParser
from app.scoring.aggregator import ScoreAggregator

router = APIRouter(prefix="/submissions", tags=["Submissions & Evaluation"])

import time

def process_submission_pipeline(sub_id: str, file_path: str, file_type: str, ps_id: Optional[str]):
    try:
        # Step 1: Parsing Slides
        DBManager.update_submission_status(sub_id, "processing", "Parsing presentation slides and layout geometry...", 25)
        time.sleep(0.3)
        
        if file_type == "pptx" or file_path.endswith(".pptx"):
            slides = PPTXParser.parse(file_path)
        else:
            slides = PDFParser.parse(file_path)

        # Step 2: Fetch Problem Statement Context
        DBManager.update_submission_status(sub_id, "processing", "Running 6-slide structure & domain alignment audit...", 50)
        time.sleep(0.4)

        ps_info = DBManager.get_problem_statement_by_id(ps_id) if ps_id else None
        ps_title = ps_info["title"] if ps_info else "General Track"
        ps_desc = ps_info["description"] if ps_info else ""

        # Step 3: Run Scoring Engine
        DBManager.update_submission_status(sub_id, "processing", "Computing local vector similarity & clarity metrics...", 75)
        report_data = ScoreAggregator.process_submission(
            slides=slides,
            ps_title=ps_title,
            ps_description=ps_desc,
            gemini_api_key=settings.GEMINI_API_KEY
        )
        time.sleep(0.4)

        # Step 4: Finalize & Save Report & Audit Trail
        DBManager.save_report(sub_id, report_data)

        # Extract text metadata for audit trail
        extracted_meta = [
            {
                "slide_number": s.get("slide_number"),
                "word_count": len(s.get("raw_text", "").split()),
                "bullet_count": s.get("bullet_count", 0),
                "text_snippet": s.get("raw_text", "")[:150]
            } for s in slides
        ]

        # Extract LLM details from raw category results if present
        tech_breakdown = report_data.get("category_breakdown", {}).get("technical_depth", {})
        llm_audit = {
            "prompt": "Structured Checklist Audit (names_specific_framework_or_language, names_specific_database_or_storage, names_specific_model_or_algorithm, describes_architecture_or_workflow)",
            "raw_response": tech_breakdown.get("raw_checklist", {})
        }

        DBManager.save_audit_trail(
            sub_id=sub_id,
            rubric_config_id=report_data.get("rubric_config_id", "sih-2026-default"),
            extracted_text_metadata={"slides": extracted_meta, "total_slides": len(slides)},
            llm_prompt_raw_response=llm_audit,
            weight_math_details=report_data.get("weight_math_details", {})
        )

    except Exception as e:
        DBManager.update_submission_status(sub_id, "failed", f"Processing error: {str(e)}", 0)

    finally:
        # Purge temporary local file so user uploads are never retained on server/local disk
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

@router.post("/upload")
async def upload_submission(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    ps_id: Optional[str] = Form(None),
    authorization: Optional[str] = Header(None)
):
    """
    Production Upload Endpoint:
    1. Validates magic bytes, file format (.pptx or .pdf), and max size (25MB).
    2. Uploads file to Supabase Cloud Storage bucket ('sih-decks').
    3. Resolves user session if Bearer token is attached.
    4. Queues background AI evaluation pipeline.
    """
    # 1. Security & Magic-byte validation
    filename, ext, file_bytes = await validate_uploaded_file(file)
    clean_ps_id = sanitize_text(ps_id, max_length=50) if ps_id else None

    # 2. Local caching for processing worker
    local_file_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(local_file_path, "wb") as f:
        f.write(file_bytes)

    # 3. Cloud Storage Upload (Supabase Bucket)
    file_url = DBManager.upload_file_to_storage(file_bytes, filename)

    # 4. Optional user identification
    user_info = extract_user_from_auth_header(authorization)
    user_email = user_info.get("email") if user_info else None

    # 5. Create persistent submission entry
    submission = DBManager.create_submission(
        file_name=filename, 
        file_type=ext, 
        file_url=file_url,
        ps_id=clean_ps_id,
        user_email=user_email
    )
    sub_id = submission["id"]

    # 6. Trigger background scoring pipeline
    background_tasks.add_task(
        process_submission_pipeline, 
        sub_id=sub_id, 
        file_path=local_file_path, 
        file_type=ext, 
        ps_id=clean_ps_id
    )

    return {
        "submission_id": sub_id,
        "status": "queued",
        "file_url": file_url,
        "message": "File uploaded and verified. AI evaluation initiated."
    }

@router.get("/{sub_id}/status")
def get_submission_status(sub_id: str):
    """
    Poll live status & stage progress of submission scanning.
    """
    sub = DBManager.get_submission(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found.")
    return sub

@router.get("/{sub_id}/report")
def get_submission_report(sub_id: str):
    """
    Get full SIH ATS score report, breakdown cards, reasons, and doc citations.
    """
    report = DBManager.get_report(sub_id)
    if not report:
        sub = DBManager.get_submission(sub_id)
        if sub and sub["status"] == "processing":
            raise HTTPException(status_code=202, detail="Report generation still in progress.")
        raise HTTPException(status_code=404, detail="Report not ready or submission failed.")
    return report

@router.get("/{sub_id}/audit_trail")
def get_submission_audit_trail(sub_id: str):
    """
    Retrieve permanent submission audit trail (extracted text, prompt/response, weight math).
    """
    audit = DBManager.get_audit_trail(sub_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit trail not found.")
    return audit


