import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import HospitalState
from app.agents.llm import get_llm
from app.config import settings

logger = logging.getLogger(__name__)


def final_clinical_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Synthesizes a cohesive, empathetic clinical response and constructs the typed
    ClinicalCarePayload for the React frontend.
    """
    symptoms = state.get("symptoms", "")
    urgency = state.get("urgency_level", "Low")
    is_emergency = state.get("is_emergency", False)
    red_flags = state.get("red_flags", [])
    dept = state.get("matched_department") or {}
    doctors = state.get("recommended_doctors", [])
    lab_tests = state.get("relevant_lab_tests", [])
    slots = state.get("available_slots", [])
    emergency_instr = state.get("emergency_instructions")
    rag_context = state.get("rag_context", "")

    # Construct typed payload for Frontend
    clinical_payload = {
        "triage": {
            "urgency_level": urgency,
            "is_emergency": is_emergency,
            "symptoms_summary": symptoms[:200],
            "primary_department": dept.get("name", "General & Internal Medicine"),
            "recommended_action": "Emergency Department Admission" if is_emergency else f"Outpatient Consultation with {dept.get('name')}",
            "red_flag_warnings": red_flags
        },
        "department": dept,
        "doctors": doctors,
        "lab_tests": lab_tests,
        "emergency_instructions": emergency_instr,
        "appointment_slots": slots
    }

    # Generate Markdown Narrative
    llm = get_llm(temperature=0.3)
    final_text = ""

    if llm:
        system_prompt = (
            "You are an empathetic, clinical AI Hospital Assistant. "
            "Address the patient's inquiry clearly and professionally.\n"
            "If it is an EMERGENCY: Urgently direct them to the ER / Ambulance hotline, do not delay care.\n"
            "If NON-EMERGENCY: Explain why the department was chosen, introduce the specialist doctor, "
            "mention recommended lab tests (with fasting notices if applicable), and explain how to book."
        )
        user_prompt = (
            f"Patient Symptoms: {symptoms}\n"
            f"Triage Level: {urgency} (Emergency: {is_emergency})\n"
            f"Red Flags: {', '.join(red_flags) if red_flags else 'None'}\n"
            f"Department: {dept.get('name')} ({dept.get('floor_location')})\n"
            f"Doctor: {doctors[0]['name'] if doctors else 'Consultant'}\n"
            f"Context: {rag_context[:300]}"
        )
        try:
            res = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
            final_text = res.content.strip()
        except Exception as e:
            logger.warning(f"LLM clinical narrative synthesis error: {e}. Falling back to template.")

    if not final_text:
        if is_emergency:
            final_text = (
                f"### 🚨 CRITICAL MEDICAL ALERT — EMERGENCY TRIAGE\n\n"
                f"Based on your symptoms, our clinical evaluation has detected **urgent red flags**:\n"
                f"* **Flagged Concerns**: {', '.join(red_flags)}\n\n"
                f"**IMMEDIATE ACTION REQUIRED:**\n"
                f"1. Please call our 24/7 Hospital Ambulance Hotline right now: **{settings.EMERGENCY_HOTLINE}**.\n"
                f"2. Proceed directly to the **Ground Floor Emergency Room (ER)**. No prior appointment is required for trauma or acute distress.\n"
                f"3. Keep the patient calm, seated, and do not administer solid food or unprescribed medication.\n\n"
                f"Our Emergency Trauma & Resuscitation Team has been notified."
            )
        else:
            lead_doc = doctors[0] if doctors else {}
            final_text = (
                f"### 🏥 Clinical Triage & Care Guidance\n\n"
                f"Based on your symptoms, we have routed you to our **{dept.get('name', 'Specialist')}** department.\n\n"
                f"#### 👨‍⚕️ Recommended Specialist\n"
                f"**{lead_doc.get('name', 'Consultant Doctor')}** — {lead_doc.get('specialization')}\n"
                f"* **Experience**: {lead_doc.get('experience_years', 10)}+ years • **Rating**: {lead_doc.get('rating', 4.8)}/5\n"
                f"* **Location**: {dept.get('floor_location', 'OPD Block')} (Ext: {dept.get('contact_ext', '101')})\n"
                f"* **Consultation Fee**: ₹{lead_doc.get('consultation_fee_inr', 800):,.0f}\n\n"
                f"#### 🧪 Recommended Diagnostic Tests\n"
            )
            for t in lab_tests[:2]:
                fast_str = "*(10-12 hrs fasting required)*" if t.get("fasting_required") else "*(No fasting)*"
                final_text += f"* **{t.get('name')}**: ₹{t.get('price_inr'):,.0f} {fast_str}\n"

            final_text += (
                f"\n#### 📅 Available Consultation Slots\n"
                f"You can confirm an appointment using the interactive cards below."
            )

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "final_care_guidance",
        "status": "completed",
        "output": f"Delivered clinical guidance with triage priority: {urgency} and department referral"
    })

    return {
        "final_response": final_text,
        "clinical_payload": clinical_payload,
        "agent_steps": steps
    }
