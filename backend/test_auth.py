import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.database.session import SessionLocal
from app.services.auth_service import AuthService
from app.database.schemas import UserRegister


def test_auth():
    print("\n--- 2. Testing Clinical Security, Bcrypt Hashing & JWT ---")

    raw_pw = "DoctorSecret2026!"
    hashed = get_password_hash(raw_pw)
    assert verify_password(raw_pw, hashed), "Password verification failed"
    assert not verify_password("WrongPassword", hashed), "Invalid password check failed"
    print("[OK] Bcrypt password hashing & verification verified.")

    token = create_access_token({"sub": "10", "email": "doctor@hospital.com"})
    assert token, "Token generation failed"
    payload = decode_access_token(token)
    assert payload.get("sub") == "10", "Token subject mismatch"
    assert payload.get("email") == "doctor@hospital.com", "Token email mismatch"
    print(f"[OK] JWT Token successfully encoded & decoded: sub={payload.get('sub')}")

    db = SessionLocal()
    try:
        import uuid
        test_email = f"patient_{uuid.uuid4().hex[:6]}@hospital.com"
        reg_data = UserRegister(
            email=test_email,
            password="SecurePatientPassword123",
            full_name="Priya Varma",
            blood_group="A+",
            emergency_contact="+91 91234 56789"
        )
        user = AuthService.register(db, reg_data)
        assert user.id is not None
        print(f"[OK] Registered patient via AuthService: {user.email}")

        auth_user = AuthService.authenticate(db, test_email, "SecurePatientPassword123")
        assert auth_user.id == user.id
        print("[OK] AuthService authentication succeeded.")

        print(">>> Clinical Authentication & Security Test Passed Successfully!\n")
    finally:
        db.close()


if __name__ == "__main__":
    test_auth()
