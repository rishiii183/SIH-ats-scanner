import os
import shutil
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException, BackgroundTasks
from typing import Optional
from app.config import settings
from app.database import DBManager
from app.security import validate_uploaded_file, extract_user_from_auth_header
from app.parsers.pptx_parser import PPTXParser
from app.parsers.pdf_parser import PDFParser
from app.scoring.aggregator import ScoreAggregator

router = APIRouter(prefix="/submissions", tags=["Submissions & Evaluation"])

def process_submission_pipeline(sub_id: str, file_path: str, file_type: str, ps_id: Optional[str]):
    try:
        # Step 1: Parsing Slides
        DBManager.update_submission_status(sub_id, "processing", "Parsing presentation slides...", 25)
        
        if file_type == "pptx" or file_path.endswith(".pptx"):
            slides = PPTXParser.parse(file_path)
        else:
            slides = PDFParser.parse(file_path)

        # Step 2: Fetch Problem Statement Context
        DBManager.update_submission_status(sub_id, "processing", "Checking problem statement alignment...", 50)
        ps_info = DBManager.get_problem_statement_by_id(ps_id) if ps_id else None
        ps_title = ps_info["title"] if ps_info else "General Track"
        ps_desc = ps_info["description"] if ps_info else ""

        # Step 3: Run Scoring Engine
        DBManager.update_submission_status(sub_id, "processing", "Evaluating technical depth & formatting...", 75)
        report_data = ScoreAggregator.process_submission(
            slides=slides,
            ps_title=ps_title,
            ps_description=ps_desc,
            gemini_api_key=settings.GEMINI_API_KEY
        )

        # Step 4: Finalize & Save Report
        DBManager.save_report(sub_id, report_data)

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
        ps_id=ps_id,
        user_email=user_email
    )
    sub_id = submission["id"]

    # 6. Trigger background scoring pipeline
    background_tasks.add_task(
        process_submission_pipeline, 
        sub_id=sub_id, 
        file_path=local_file_path, 
        file_type=ext, 
        ps_id=ps_id
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

