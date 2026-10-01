from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import LabTest
from app.database.schemas import LabTestResponse

router = APIRouter(prefix="/lab-tests", tags=["Laboratory & Diagnostic Tests"])


@router.get("", response_model=List[LabTestResponse])
def get_lab_tests(
    query: Optional[str] = Query(None),
    sample_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve diagnostic laboratory and imaging tests."""
    q = db.query(LabTest)
    if sample_type:
        q = q.filter(LabTest.sample_type.ilike(f"%{sample_type}%"))
    if query:
        q = q.filter(
            (LabTest.name.ilike(f"%{query}%")) |
            (LabTest.description.ilike(f"%{query}%"))
        )
    return q.all()
