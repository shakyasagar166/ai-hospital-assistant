import logging
from typing import Dict, Any, List
from app.agents.state import HospitalState
from app.database.session import SessionLocal
from app.database.models import Doctor, LabTest

logger = logging.getLogger(__name__)


def doctor_matching_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Matches patient with specialist doctors and suggests relevant diagnostic lab tests.
    """
    matched_dept = state.get("matched_department")
    if not matched_dept:
        return {"recommended_doctors": [], "relevant_lab_tests": []}

    dept_id = matched_dept["id"]
    db = SessionLocal()

    doctors = []
    lab_tests = []
    try:
        doc_records = db.query(Doctor).filter(Doctor.department_id == dept_id).order_by(Doctor.rating.desc()).all()
        for doc in doc_records:
            doctors.append({
                "id": doc.id,
                "name": doc.name,
                "specialization": doc.specialization,
                "qualification": doc.qualification,
                "experience_years": doc.experience_years,
                "consultation_fee_inr": doc.consultation_fee_inr,
                "rating": doc.rating,
                "available_days": doc.available_days_json or [],
                "available_hours": doc.available_hours,
                "image_url": doc.image_url
            })

        # Fetch tests in this department
        test_records = db.query(LabTest).filter(LabTest.department_id == dept_id).all()
        if not test_records:
            test_records = db.query(LabTest).limit(3).all()

        for t in test_records:
            lab_tests.append({
                "id": t.id,
                "name": t.name,
                "sample_type": t.sample_type,
                "fasting_required": t.fasting_required,
                "turnaround_hours": t.turnaround_hours,
                "price_inr": t.price_inr,
                "description": t.description
            })
    finally:
        db.close()

    steps = state.get("agent_steps", [])
    doc_count = len(doctors)
    primary_doc = doctors[0]["name"] if doctors else "Staff Physician"
    steps.append({
        "agent": "doctor_matching",
        "status": "completed",
        "output": f"Matched {doc_count} specialist doctors. Lead Consultant: {primary_doc} | {len(lab_tests)} diagnostic tests identified"
    })

    return {
        "recommended_doctors": doctors,
        "relevant_lab_tests": lab_tests,
        "agent_steps": steps
    }
