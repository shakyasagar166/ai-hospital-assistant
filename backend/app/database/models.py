import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="patient")  # patient, doctor, staff, admin
    blood_group = Column(String(10), default="O+")
    emergency_contact = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    floor_location = Column(String(100), nullable=False)
    head_doctor = Column(String(255), nullable=True)
    contact_ext = Column(String(50), default="101")
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    doctors = relationship("Doctor", back_populates="department", cascade="all, delete-orphan")
    lab_tests = relationship("LabTest", back_populates="department")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False, index=True)
    qualification = Column(String(255), nullable=False)
    experience_years = Column(Integer, nullable=False)
    consultation_fee_inr = Column(Float, nullable=False)
    rating = Column(Float, default=4.8)
    available_days_json = Column(JSON, default=list)
    available_hours = Column(String(100), default="09:00 AM - 05:00 PM")
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    appointment_date = Column(String(50), nullable=False)
    time_slot = Column(String(50), nullable=False)
    status = Column(String(50), default="confirmed")  # confirmed, pending, completed, cancelled
    symptoms_summary = Column(Text, nullable=True)
    triage_level = Column(String(50), default="Low")  # Low, Medium, Urgent, Emergency
    confirmation_code = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    patient = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False, index=True)
    sample_type = Column(String(100), nullable=False)
    fasting_required = Column(Boolean, default=False)
    turnaround_hours = Column(Integer, default=24)
    price_inr = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    department = relationship("Department", back_populates="lab_tests")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    title = Column(String(255), default="New Clinical Inquiry")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(64), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    agent_steps_json = Column(JSON, default=list)
    triage_payload_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
