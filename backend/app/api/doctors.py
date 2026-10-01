from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Doctor, Department
from app.database.schemas import DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors & Specialists"])


@router.get("", response_model=List[DoctorResponse])
def get_doctors(
    department_id: Optional[int] = Query(None),
    specialization: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve specialist doctors with optional department and specialization filters."""
    q = db.query(Doctor)
    if department_id:
        q = q.filter(Doctor.department_id == department_id)
    if specialization:
        q = q.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    if query:
        q = q.filter(
            (Doctor.name.ilike(f"%{query}%")) |
            (Doctor.specialization.ilike(f"%{query}%"))
        )
    return q.order_by(Doctor.rating.desc()).all()


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Retrieve individual doctor profile and availability."""
    doc = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    return doc
