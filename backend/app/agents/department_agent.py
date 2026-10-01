import logging
from typing import Dict, Any
from app.agents.state import HospitalState
from app.database.session import SessionLocal
from app.database.models import Department

logger = logging.getLogger(__name__)


def department_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Finds and resolves the medical department responsible for the patient's care.
    """
    target = state.get("target_department") or "General & Internal Medicine"

    db = SessionLocal()
    matched = None
    try:
        dept = db.query(Department).filter(
            (Department.name.ilike(f"%{target}%")) |
            (Department.description.ilike(f"%{target}%"))
        ).first()

        if not dept:
            dept = db.query(Department).first()

        if dept:
            matched = {
                "id": dept.id,
                "name": dept.name,
                "floor_location": dept.floor_location,
                "head_doctor": dept.head_doctor,
                "contact_ext": dept.contact_ext,
                "description": dept.description,
                "image_url": dept.image_url
            }
    finally:
        db.close()

    steps = state.get("agent_steps", [])
    dept_name = matched["name"] if matched else "General Medicine"
    dept_floor = matched["floor_location"] if matched else "Ground Floor"
    steps.append({
        "agent": "department_routing",
        "status": "completed",
        "output": f"Assigned Department: {dept_name} ({dept_floor}, Ext: {matched.get('contact_ext') if matched else '101'})"
    })

    return {
        "matched_department": matched,
        "agent_steps": steps
    }
