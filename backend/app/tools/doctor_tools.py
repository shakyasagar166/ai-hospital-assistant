from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.database.session import SessionLocal
from app.database.models import Doctor, Department


@tool
def search_doctors(
    department_name: Optional[str] = None,
    specialization: Optional[str] = None,
    query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search specialist doctors by department, clinical specialization, or name.
    """
    db = SessionLocal()
    try:
        q = db.query(Doctor).join(Department)
        if department_name:
            q = q.filter(Department.name.ilike(f"%{department_name}%"))
        if specialization:
            q = q.filter(Doctor.specialization.ilike(f"%{specialization}%"))
        if query:
            q = q.filter(
                (Doctor.name.ilike(f"%{query}%")) |
                (Doctor.specialization.ilike(f"%{query}%")) |
                (Department.name.ilike(f"%{query}%"))
            )

        doctors = q.order_by(Doctor.rating.desc()).all()
        return [
            {
                "id": doc.id,
                "name": doc.name,
                "department": doc.department.name,
                "specialization": doc.specialization,
                "qualification": doc.qualification,
                "experience_years": doc.experience_years,
                "consultation_fee_inr": doc.consultation_fee_inr,
                "rating": doc.rating,
                "available_days": doc.available_days_json or [],
                "available_hours": doc.available_hours
            }
            for doc in doctors
        ]
    finally:
        db.close()


@tool
def get_doctor_availability(doctor_id: int) -> Dict[str, Any]:
    """
    Retrieves working schedule, consultation hours, and open time slots for a doctor.
    """
    db = SessionLocal()
    try:
        doc = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doc:
            return {"error": f"Doctor with ID {doctor_id} not found"}

        return {
            "doctor_id": doc.id,
            "name": doc.name,
            "available_days": doc.available_days_json or [],
            "available_hours": doc.available_hours,
            "sample_slots": ["09:30 AM", "11:00 AM", "02:30 PM", "04:00 PM"],
            "consultation_fee_inr": doc.consultation_fee_inr
        }
    finally:
        db.close()
