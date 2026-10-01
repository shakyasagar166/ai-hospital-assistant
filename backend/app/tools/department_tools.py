from typing import List, Dict, Any
from langchain_core.tools import tool
from app.database.session import SessionLocal
from app.database.models import Department


@tool
def search_departments(query: str) -> List[Dict[str, Any]]:
    """
    Search hospital medical departments by name or clinical scope (e.g. Cardiology, Neurology, Orthopedics).
    """
    db = SessionLocal()
    try:
        q = db.query(Department).filter(
            (Department.name.ilike(f"%{query}%")) |
            (Department.description.ilike(f"%{query}%"))
        )
        departments = q.all()
        return [
            {
                "id": d.id,
                "name": d.name,
                "floor_location": d.floor_location,
                "head_doctor": d.head_doctor,
                "contact_ext": d.contact_ext,
                "description": d.description[:140] + "..."
            }
            for d in departments
        ]
    finally:
        db.close()


@tool
def get_department_details(department_id: int) -> Dict[str, Any]:
    """
    Retrieves full details of a hospital department by its ID including doctors and location.
    """
    db = SessionLocal()
    try:
        dept = db.query(Department).filter(Department.id == department_id).first()
        if not dept:
            return {"error": f"Department with ID {department_id} not found"}
        return {
            "id": dept.id,
            "name": dept.name,
            "floor_location": dept.floor_location,
            "head_doctor": dept.head_doctor,
            "contact_ext": dept.contact_ext,
            "description": dept.description,
            "doctor_count": len(dept.doctors)
        }
    finally:
        db.close()
