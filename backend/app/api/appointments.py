import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Appointment, Doctor, User
from app.database.schemas import AppointmentCreate, AppointmentResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appt_in: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Books a medical consultation appointment."""
    doctor = db.query(Doctor).filter(Doctor.id == appt_in.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    code = f"MED-{uuid.uuid4().hex[:8].upper()}"
    appt = Appointment(
        patient_id=current_user.id,
        doctor_id=appt_in.doctor_id,
        appointment_date=appt_in.appointment_date,
        time_slot=appt_in.time_slot,
        status="confirmed",
        symptoms_summary=appt_in.symptoms_summary,
        triage_level=appt_in.triage_level or "Low",
        confirmation_code=code
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.get("", response_model=List[AppointmentResponse])
def get_my_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lists all consultation appointments for the authenticated patient."""
    return db.query(Appointment).filter(Appointment.patient_id == current_user.id).order_by(Appointment.created_at.desc()).all()


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancels a scheduled appointment."""
    appt = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.patient_id == current_user.id).first()
    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    appt.status = "cancelled"
    db.commit()
    return None
