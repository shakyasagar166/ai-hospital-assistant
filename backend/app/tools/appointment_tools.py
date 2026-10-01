import uuid
from typing import Dict, Any, List
from langchain_core.tools import tool
from app.database.session import SessionLocal
from app.database.models import Appointment, Doctor, User


@tool
def book_appointment_tool(
    patient_id: int,
    doctor_id: int,
    appointment_date: str,
    time_slot: str,
    symptoms: str = "",
    triage_level: str = "Low"
) -> Dict[str, Any]:
    """
    Books a confirmed medical consultation appointment with a doctor for a patient.
    """
    db = SessionLocal()
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            return {"error": f"Doctor ID {doctor_id} not found"}

        code = f"MED-{uuid.uuid4().hex[:8].upper()}"
        appt = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            time_slot=time_slot,
            status="confirmed",
            symptoms_summary=symptoms,
            triage_level=triage_level,
            confirmation_code=code
        )
        db.add(appt)
        db.commit()
        db.refresh(appt)

        return {
            "appointment_id": appt.id,
            "confirmation_code": code,
            "doctor_name": doctor.name,
            "department": doctor.department.name,
            "appointment_date": appointment_date,
            "time_slot": time_slot,
            "consultation_fee_inr": doctor.consultation_fee_inr,
            "floor_location": doctor.department.floor_location,
            "status": "confirmed"
        }
    finally:
        db.close()


@tool
def get_patient_appointments(patient_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves previous and upcoming appointments for a patient.
    """
    db = SessionLocal()
    try:
        appts = db.query(Appointment).filter(Appointment.patient_id == patient_id).order_by(Appointment.created_at.desc()).all()
        return [
            {
                "id": a.id,
                "doctor_name": a.doctor.name if a.doctor else "Unknown Doctor",
                "department": a.doctor.department.name if a.doctor and a.doctor.department else "General",
                "appointment_date": a.appointment_date,
                "time_slot": a.time_slot,
                "status": a.status,
                "confirmation_code": a.confirmation_code
            }
            for a in appts
        ]
    finally:
        db.close()
