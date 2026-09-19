from fastapi import APIRouter, Query
from typing import Optional, List
from app.database import DBManager
from app.security import sanitize_text

router = APIRouter(prefix="/problem-statements", tags=["Problem Statements"])

@router.get("", response_model=List[dict])
def list_problem_statements(q: Optional[str] = Query(None, description="Search query by PS ID or Title")):
    """
    Search available SIH official problem statements bank with sanitized input.
    """
    clean_q = sanitize_text(q, max_length=100) if q else None
    return DBManager.get_problem_statements(query=clean_q)

