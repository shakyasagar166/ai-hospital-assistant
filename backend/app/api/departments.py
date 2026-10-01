from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Department
from app.database.schemas import DepartmentResponse, DepartmentDetailResponse

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=List[DepartmentResponse])
def get_departments(
    query: Optional[str] = Query(None, description="Search by name or clinical scope"),
    db: Session = Depends(get_db)
):
    """Retrieve all hospital medical departments."""
    q = db.query(Department)
    if query:
        q = q.filter(
            (Department.name.ilike(f"%{query}%")) |
            (Department.description.ilike(f"%{query}%"))
        )
    return q.all()


@router.get("/{department_id}", response_model=DepartmentDetailResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    """Retrieve department details with doctors list."""
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found"
        )
    return dept
