import re
from typing import Dict, Any, List
from langchain_core.tools import tool
from app.database.session import SessionLocal
from app.database.models import LabTest, Department


@tool
def evaluate_triage_urgency(symptoms: str) -> Dict[str, Any]:
    """
    Evaluates clinical urgency level (Low, Medium, Urgent, Emergency) and detects life-threatening red flags.
    """
    s_lower = symptoms.lower()
    red_flags = []
    urgency = "Low"
    is_emergency = False
    suggested_dept = "General & Internal Medicine"

    # 1. Cardiac Red Flags
    if any(k in s_lower for k in ["chest pain", "pressure on chest", "left arm pain", "heart attack", "crushing chest", "palpitations with dizziness"]):
        red_flags.append("Acute Cardiovascular Distress / Possible Angina or Myocardial Infarction")
        urgency = "Emergency"
        is_emergency = True
        suggested_dept = "Cardiology"

    # 2. Neurological Stroke FAST Red Flags
    elif any(k in s_lower for k in ["facial drooping", "face droop", "slurred speech", "loss of speech", "sudden paralysis", "one side weakness", "stroke"]):
        red_flags.append("Suspected Acute Ischemic / Hemorrhagic Stroke (FAST Protocol)")
        urgency = "Emergency"
        is_emergency = True
        suggested_dept = "Neurology & Neurosurgery"

    # 3. Severe Respiratory Distress
    elif any(k in s_lower for k in ["cannot breathe", "severe breathlessness", "gasping for air", "choking", "blue lips"]):
        red_flags.append("Severe Acute Respiratory Distress")
        urgency = "Emergency"
        is_emergency = True
        suggested_dept = "Pulmonology & Respiratory Medicine"

    # 4. Urgent / High Priority Symptoms
    elif any(k in s_lower for k in ["fracture", "broken bone", "high fever with rash", "severe abdominal pain", "blood in stool", "blood in vomit"]):
        urgency = "Urgent"
        if "bone" in s_lower or "fracture" in s_lower or "joint" in s_lower:
            suggested_dept = "Orthopedics & Joint Replacement"
        elif "abdominal" in s_lower or "vomit" in s_lower:
            suggested_dept = "Gastroenterology & Hepatology"
        else:
            suggested_dept = "General & Internal Medicine"

    # 5. Routine / Medium Priority
    elif any(k in s_lower for k in ["headache", "migraine", "dizziness", "numbness"]):
        urgency = "Medium"
        suggested_dept = "Neurology & Neurosurgery"
    elif any(k in s_lower for k in ["skin", "rash", "acne", "hair loss", "itching", "eczema"]):
        urgency = "Low"
        suggested_dept = "Dermatology & Skin Health"
    elif any(k in s_lower for k in ["child", "baby", "infant", "kid", "vaccination", "pediatric"]):
        urgency = "Medium"
        suggested_dept = "Pediatrics & Child Care"
    elif any(k in s_lower for k in ["cough", "wheezing", "asthma", "phlegm", "breath"]):
        urgency = "Medium"
        suggested_dept = "Pulmonology & Respiratory Medicine"
    elif any(k in s_lower for k in ["stomach", "gastric", "acid", "reflux", "constipation", "diarrhea"]):
        urgency = "Medium"
        suggested_dept = "Gastroenterology & Hepatology"
    elif any(k in s_lower for k in ["knee", "back pain", "spine", "arthritis", "joint pain", "shoulder"]):
        urgency = "Medium"
        suggested_dept = "Orthopedics & Joint Replacement"

    action = (
        "IMMEDIATE EMERGENCY: Proceed to Ground Floor Emergency Room (ER) or call Ambulance Hotline 108/102 immediately."
        if is_emergency
        else f"Consult a specialist in {suggested_dept}. An outpatient appointment is recommended."
    )

    return {
        "urgency_level": urgency,
        "is_emergency": is_emergency,
        "primary_department": suggested_dept,
        "red_flag_warnings": red_flags,
        "recommended_action": action
    }


@tool
def search_lab_tests_tool(query: str, department_name: str = "") -> List[Dict[str, Any]]:
    """
    Searches diagnostic laboratory tests by name or department.
    """
    db = SessionLocal()
    try:
        q = db.query(LabTest)
        if query:
            q = q.filter(
                (LabTest.name.ilike(f"%{query}%")) |
                (LabTest.description.ilike(f"%{query}%"))
            )
        tests = q.limit(5).all()
        return [
            {
                "id": t.id,
                "name": t.name,
                "sample_type": t.sample_type,
                "fasting_required": t.fasting_required,
                "turnaround_hours": t.turnaround_hours,
                "price_inr": t.price_inr,
                "description": t.description
            }
            for t in tests
        ]
    finally:
        db.close()
