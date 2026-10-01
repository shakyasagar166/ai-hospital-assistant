import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.tools.department_tools import search_departments, get_department_details
from app.tools.doctor_tools import search_doctors, get_doctor_availability
from app.tools.triage_tools import evaluate_triage_urgency, search_lab_tests_tool
from app.tools.appointment_tools import book_appointment_tool


def test_tools():
    print("\n--- 4. Testing Hospital Tool Calling Layer ---")

    # 1. evaluate_triage_urgency
    res_emer = evaluate_triage_urgency.invoke({"symptoms": "Severe crushing chest pain radiating to left arm and breathlessness"})
    assert res_emer["is_emergency"] is True
    assert res_emer["urgency_level"] == "Emergency"
    print(f"[OK] evaluate_triage_urgency (Emergency): {res_emer['urgency_level']} -> {res_emer['primary_department']}")

    res_routine = evaluate_triage_urgency.invoke({"symptoms": "Mild skin rash and itching on arms"})
    assert res_routine["is_emergency"] is False
    print(f"[OK] evaluate_triage_urgency (Routine): {res_routine['urgency_level']} -> {res_routine['primary_department']}")

    # 2. search_departments
    depts = search_departments.invoke({"query": "Cardiology"})
    assert len(depts) > 0
    print(f"[OK] search_departments found: {depts[0]['name']} ({depts[0]['floor_location']})")

    # 3. search_doctors
    docs = search_doctors.invoke({"department_name": "Cardiology"})
    assert len(docs) > 0
    print(f"[OK] search_doctors found: {docs[0]['name']} - {docs[0]['specialization']}")

    # 4. get_doctor_availability
    avail = get_doctor_availability.invoke({"doctor_id": docs[0]["id"]})
    assert "sample_slots" in avail
    print(f"[OK] get_doctor_availability slots: {avail['sample_slots']}")

    # 5. search_lab_tests_tool
    tests = search_lab_tests_tool.invoke({"query": "Lipid Profile"})
    assert len(tests) > 0
    print(f"[OK] search_lab_tests_tool found: {tests[0]['name']} (Fasting: {tests[0]['fasting_required']})")

    # 6. book_appointment_tool
    booked = book_appointment_tool.invoke({
        "patient_id": 1,
        "doctor_id": docs[0]["id"],
        "appointment_date": "2026-10-20",
        "time_slot": "11:00 AM",
        "symptoms": "Annual cardiac health review",
        "triage_level": "Low"
    })
    assert "confirmation_code" in booked
    print(f"[OK] book_appointment_tool confirmed: Code {booked['confirmation_code']} with {booked['doctor_name']}")

    print(">>> Hospital Tool Calling Layer Test Passed Successfully!\n")


if __name__ == "__main__":
    test_tools()
