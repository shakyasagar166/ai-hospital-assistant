import logging
from typing import Dict, Any, List
from app.agents.state import HospitalState

logger = logging.getLogger(__name__)


def schedule_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Compiles open consultation appointment slots for the patient.
    """
    doctors = state.get("recommended_doctors", [])
    primary_doc = doctors[0] if doctors else None
    hours = primary_doc.get("available_hours", "09:00 AM - 05:00 PM") if primary_doc else "09:00 AM - 05:00 PM"

    slots = [
        "10:00 AM - 10:30 AM",
        "11:30 AM - 12:00 PM",
        "02:30 PM - 03:00 PM",
        "04:00 PM - 04:30 PM"
    ]

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "appointment_scheduler",
        "status": "completed",
        "output": f"Generated {len(slots)} available consultation slots ({hours})"
    })

    return {
        "available_slots": slots,
        "agent_steps": steps
    }
