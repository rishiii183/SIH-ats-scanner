from fastapi import APIRouter, Query
from typing import Optional, List
from app.database import DBManager

router = APIRouter(prefix="/problem-statements", tags=["Problem Statements"])

@router.get("", response_model=List[dict])
def list_problem_statements(q: Optional[str] = Query(None, description="Search query by PS ID or Title")):
    """
    Search available SIH official problem statements bank.
    """
    return DBManager.get_problem_statements(query=q)
