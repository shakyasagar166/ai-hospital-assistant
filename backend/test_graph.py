import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.graph.hospital_graph import hospital_app


def test_graph():
    print("\n--- 5. Testing LangGraph Clinical Multi-Agent Workflow ---")

    test_query = "I have been experiencing acute chest pain radiating to my shoulder with shortness of breath."
    print(f"Patient Query: '{test_query}'\n")

    initial_state = {
        "patient_query": test_query,
        "user_id": 1,
        "agent_steps": []
    }

    final_state = hospital_app.invoke(initial_state)

    print("--- Executed Clinical Multi-Agent Steps ---")
    for step in final_state.get("agent_steps", []):
        print(f"-> [{step['agent']}]: {step['output']}")

    assert final_state.get("is_emergency") is True, "Expected emergency flag to be True"
    assert final_state.get("urgency_level") == "Emergency", f"Expected Emergency, got {final_state.get('urgency_level')}"
    assert final_state.get("clinical_payload") is not None, "Clinical payload missing"

    payload = final_state.get("clinical_payload")
    print(f"\n[OK] Triage Priority: {payload['triage']['urgency_level']}")
    print(f"[OK] Department Assigned: {payload['triage']['primary_department']}")
    print(f"[OK] Doctors matched: {len(payload['doctors'])}")
    print(f"[OK] Emergency Instructions present: {bool(payload.get('emergency_instructions'))}")

    print(">>> LangGraph Clinical Multi-Agent Workflow Test Passed Successfully!\n")


if __name__ == "__main__":
    test_graph()
