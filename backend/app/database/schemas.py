from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    role: Optional[str] = "patient"
    blood_group: Optional[str] = "O+"
    emergency_contact: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    blood_group: Optional[str] = "O+"
    emergency_contact: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None


# --- Department & Doctor Schemas ---
class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str
    floor_location: str
    head_doctor: Optional[str] = None
    contact_ext: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class DoctorResponse(BaseModel):
    id: int
    department_id: int
    name: str
    specialization: str
    qualification: str
    experience_years: int
    consultation_fee_inr: float
    rating: float
    available_days: List[str] = Field(default_factory=list, alias="available_days_json")
    available_hours: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class DepartmentDetailResponse(DepartmentResponse):
    doctors: List[DoctorResponse] = []


# --- Diagnostic Lab Test Schemas ---
class LabTestResponse(BaseModel):
    id: int
    name: str
    sample_type: str
    fasting_required: bool
    turnaround_hours: int
    price_inr: float
    description: Optional[str] = None

    class Config:
        from_attributes = True


# --- Appointment Schemas ---
class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: str
    time_slot: str
    symptoms_summary: Optional[str] = None
    triage_level: Optional[str] = "Low"


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: str
    time_slot: str
    status: str
    symptoms_summary: Optional[str] = None
    triage_level: str
    confirmation_code: str
    doctor: Optional[DoctorResponse] = None

    class Config:
        from_attributes = True


# --- Clinical Triage & Chat Schemas ---
class TriageAssessment(BaseModel):
    urgency_level: str  # Low, Medium, Urgent, Emergency
    is_emergency: bool
    symptoms_summary: str
    primary_department: str
    recommended_action: str
    red_flag_warnings: List[str] = []


class ClinicalCarePayload(BaseModel):
    triage: TriageAssessment
    department: Optional[Dict[str, Any]] = None
    doctors: List[Dict[str, Any]] = []
    lab_tests: List[Dict[str, Any]] = []
    emergency_instructions: Optional[str] = None
    appointment_slots: List[str] = []


class AgentStep(BaseModel):
    agent: str
    status: str = "completed"
    output: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    clinical_payload: Optional[ClinicalCarePayload] = None
    agent_steps: List[AgentStep] = []
