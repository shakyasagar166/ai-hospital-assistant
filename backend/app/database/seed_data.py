import json
import logging
import os
import uuid
from sqlalchemy.orm import Session
from app.database.models import User, Department, Doctor, LabTest, Appointment
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def seed_database(db: Session):
    """
    Seeds database with initial medical departments, specialist doctors, lab tests, and demo patient.
    """
    # 1. Seed Demo Patient User
    demo_user = db.query(User).filter(User.email == "patient@hospital.com").first()
    if not demo_user:
        logger.info("Creating demo patient: patient@hospital.com / Password123!")
        demo_user = User(
            email="patient@hospital.com",
            hashed_password=get_password_hash("Password123!"),
            full_name="Aarav Sharma",
            role="patient",
            blood_group="B+",
            emergency_contact="+91 98765 43210",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

    # 2. Seed Departments, Doctors, Lab Tests
    existing_dept = db.query(Department).first()
    if existing_dept:
        logger.info("Hospital database already seeded. Skipping.")
        return

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root_dir = os.path.dirname(backend_dir)
    possible_paths = [
        os.path.join(root_dir, "data", "hospital_data.json"),
        os.path.join(backend_dir, "data", "hospital_data.json"),
        os.path.join(os.getcwd(), "data", "hospital_data.json"),
    ]
    json_path = None
    for p in possible_paths:
        if os.path.exists(p):
            json_path = p
            break

    if not json_path:
        logger.warning(f"Hospital data file not found in possible locations: {possible_paths}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"Seeding hospital data from {json_path}...")

    # Seed Departments
    dept_map = {}
    for d in data.get("departments", []):
        dept = Department(
            name=d["name"],
            description=d["description"],
            floor_location=d["floor_location"],
            head_doctor=d.get("head_doctor"),
            contact_ext=d.get("contact_ext", "101"),
            image_url=d.get("image_url")
        )
        db.add(dept)
        db.flush()
        dept_map[dept.name] = dept.id

    # Seed Doctors
    for doc in data.get("doctors", []):
        dept_id = dept_map.get(doc.get("department"))
        if not dept_id and dept_map:
            dept_id = list(dept_map.values())[0]

        d_obj = Doctor(
            department_id=dept_id,
            name=doc["name"],
            specialization=doc["specialization"],
            qualification=doc["qualification"],
            experience_years=doc["experience_years"],
            consultation_fee_inr=doc["consultation_fee_inr"],
            rating=doc.get("rating", 4.8),
            available_days_json=doc.get("available_days", []),
            available_hours=doc.get("available_hours", "09:00 AM - 05:00 PM"),
            image_url=doc.get("image_url")
        )
        db.add(d_obj)

    # Seed Lab Tests
    for test in data.get("lab_tests", []):
        dept_id = dept_map.get(test.get("department"))
        t_obj = LabTest(
            department_id=dept_id,
            name=test["name"],
            sample_type=test["sample_type"],
            fasting_required=test.get("fasting_required", False),
            turnaround_hours=test.get("turnaround_hours", 24),
            price_inr=test["price_inr"],
            description=test.get("description")
        )
        db.add(t_obj)

    db.commit()

    # Seed Sample Confirmed Appointment for Demo Patient
    first_doc = db.query(Doctor).first()
    if demo_user and first_doc:
        sample_appt = Appointment(
            patient_id=demo_user.id,
            doctor_id=first_doc.id,
            appointment_date="2026-10-15",
            time_slot="10:30 AM",
            status="confirmed",
            symptoms_summary="Routine cardiac wellness checkup and blood pressure monitoring",
            triage_level="Low",
            confirmation_code=f"MED-{uuid.uuid4().hex[:8].upper()}"
        )
        db.add(sample_appt)
        db.commit()

    logger.info("Hospital database successfully initialized and seeded!")
