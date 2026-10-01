import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.database.session import init_db, SessionLocal
from app.database.models import Department, Doctor, LabTest, User, Appointment
from app.database.seed_data import seed_database


def test_database():
    print("\n--- 1. Testing Hospital Database Initialization & Models ---")
    init_db()
    db = SessionLocal()
    try:
        seed_database(db)

        # Verify departments
        dept_count = db.query(Department).count()
        print(f"[OK] Departments count: {dept_count}")
        assert dept_count >= 8, f"Expected at least 8 departments, got {dept_count}"

        # Verify doctors
        doc_count = db.query(Doctor).count()
        print(f"[OK] Doctors count: {doc_count}")
        assert doc_count >= 12, f"Expected at least 12 doctors, got {doc_count}"

        # Verify lab tests
        lab_count = db.query(LabTest).count()
        print(f"[OK] Lab tests count: {lab_count}")
        assert lab_count >= 10, f"Expected at least 10 lab tests, got {lab_count}"

        # Verify demo patient
        user = db.query(User).filter(User.email == "patient@hospital.com").first()
        assert user is not None, "Demo patient not found"
        print(f"[OK] Demo patient verified: {user.full_name} ({user.email}) - Blood: {user.blood_group}")

        # Verify sample appointment
        appt = db.query(Appointment).filter(Appointment.patient_id == user.id).first()
        assert appt is not None, "Sample appointment not found"
        print(f"[OK] Sample appointment verified: Code {appt.confirmation_code} with Doctor ID {appt.doctor_id}")

        print(">>> Hospital Database Models & Seeding Test Passed Successfully!\n")
    finally:
        db.close()


if __name__ == "__main__":
    test_database()
