import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api():
    print("\n--- 6. Testing FastAPI Clinical REST & Chat Endpoints ---")

    # 1. Health
    res = client.get("/health")
    assert res.status_code == 200
    print(f"[OK] /health: {res.json()['status']}")

    # 2. Departments
    res = client.get("/api/v1/departments")
    assert res.status_code == 200
    depts = res.json()
    assert len(depts) >= 8
    print(f"[OK] GET /departments: retrieved {len(depts)} clinical departments")

    # 3. Doctors
    res = client.get("/api/v1/doctors")
    assert res.status_code == 200
    docs = res.json()
    assert len(docs) >= 10
    print(f"[OK] GET /doctors: retrieved {len(docs)} specialist doctors")

    # 4. Lab Tests
    res = client.get("/api/v1/lab-tests")
    assert res.status_code == 200
    tests = res.json()
    assert len(tests) >= 10
    print(f"[OK] GET /lab-tests: retrieved {len(tests)} diagnostic tests")

    # 5. Auth Login
    res = client.post("/api/v1/auth/login", json={"email": "patient@hospital.com", "password": "Password123!"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    print("[OK] POST /auth/login: Patient login succeeded, clinical JWT obtained.")

    # 6. Auth Me
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    print(f"[OK] GET /auth/me: {res.json()['full_name']} (Blood Group: {res.json()['blood_group']})")

    # 7. Clinical Chat Endpoint
    chat_payload = {
        "message": "I have had a high fever, body aches and dry cough for 3 days",
        "conversation_id": None
    }
    res = client.post("/api/v1/chat", json=chat_payload)
    assert res.status_code == 200
    chat_res = res.json()
    assert "conversation_id" in chat_res
    assert "clinical_payload" in chat_res
    print("[OK] POST /chat: Clinical assistant response received:")
    print(f"   - Conversation ID: {chat_res['conversation_id']}")
    print(f"   - Triage Urgency: {chat_res['clinical_payload']['triage']['urgency_level']}")
    print(f"   - Matched Department: {chat_res['clinical_payload']['department']['name']}")
    print(f"   - Agent Steps executed: {len(chat_res['agent_steps'])}")

    print(">>> FastAPI Clinical REST & Chat Endpoints Test Passed Successfully!\n")


if __name__ == "__main__":
    test_api()
