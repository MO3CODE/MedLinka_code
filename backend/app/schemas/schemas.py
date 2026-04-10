"""
MedLinka — Pydantic Schemas
Request validation + response serialization for all endpoints
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models import (
    UserRole, Language, DoctorSpecialty,
    AppointmentStatus, AppointmentType,
    OrderStatus, ReminderFrequency,
)


# ─────────────────────────────────────────────────────────────
# Base helpers
# ─────────────────────────────────────────────────────────────

class OKResponse(BaseModel):
    message: str
    data: Optional[dict] = None


# ─────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    full_name: str = Field(min_length=2, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=30)
    role: UserRole = UserRole.PATIENT
    preferred_language: Language = Language.AR

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)


# ─────────────────────────────────────────────────────────────
# User
# ─────────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    role: UserRole
    preferred_language: Language
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = Field(default=None, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=30)
    preferred_language: Optional[Language] = None
    expo_push_token: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# Doctor Profile
# ─────────────────────────────────────────────────────────────

class DoctorProfileCreate(BaseModel):
    specialty: DoctorSpecialty = DoctorSpecialty.GENERAL
    bio_ar: Optional[str] = None
    bio_tr: Optional[str] = None
    bio_en: Optional[str] = None
    years_experience: int = Field(default=0, ge=0, le=60)
    consultation_fee: float = Field(default=0.0, ge=0)
    available_days: Optional[str] = None   # "mon,tue,wed"
    available_from: Optional[str] = None   # "09:00"
    available_to: Optional[str] = None     # "17:00"


class DoctorProfileOut(BaseModel):
    id: str
    user_id: str
    specialty: DoctorSpecialty
    bio_ar: Optional[str]
    bio_tr: Optional[str]
    bio_en: Optional[str]
    years_experience: int
    consultation_fee: float
    rating: float
    total_reviews: int
    is_available: bool
    available_days: Optional[str]
    available_from: Optional[str]
    available_to: Optional[str]
    user: UserOut

    model_config = {"from_attributes": True}


class DoctorListItem(BaseModel):
    id: str
    specialty: DoctorSpecialty
    rating: float
    consultation_fee: float
    is_available: bool
    years_experience: int
    user: UserOut

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────────
# Medicine
# ─────────────────────────────────────────────────────────────

class MedicineCreate(BaseModel):
    name_ar: str = Field(min_length=1, max_length=200)
    name_tr: Optional[str] = Field(default=None, max_length=200)
    name_en: Optional[str] = Field(default=None, max_length=200)
    description_ar: Optional[str] = None
    description_tr: Optional[str] = None
    description_en: Optional[str] = None
    category: Optional[str] = Field(default=None, max_length=100)
    price: float = Field(gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    requires_prescription: bool = False


class MedicineOut(BaseModel):
    id: str
    pharmacy_id: str
    name_ar: str
    name_tr: Optional[str]
    name_en: Optional[str]
    description_ar: Optional[str]
    description_tr: Optional[str]
    description_en: Optional[str]
    category: Optional[str]
    price: float
    stock_quantity: int
    image_url: Optional[str]
    requires_prescription: bool
    is_active: bool

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────────
# Appointment
# ─────────────────────────────────────────────────────────────

class AppointmentCreate(BaseModel):
    doctor_id: str
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, ge=15, le=120)
    type: AppointmentType = AppointmentType.CHAT
    notes_by_patient: Optional[str] = Field(default=None, max_length=1000)


class AppointmentOut(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    scheduled_at: datetime
    duration_minutes: int
    type: AppointmentType
    status: AppointmentStatus
    notes_by_patient: Optional[str]
    notes_by_doctor: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class DoctorNoteUpdate(BaseModel):
    notes_by_doctor: str = Field(max_length=2000)
    status: Optional[AppointmentStatus] = None


# ─────────────────────────────────────────────────────────────
# Order
# ─────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    medicine_id: str
    quantity: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(min_length=1)
    delivery_address: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=500)


class OrderItemOut(BaseModel):
    id: str
    medicine_id: str
    quantity: int
    unit_price: float
    medicine: MedicineOut

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: str
    patient_id: str
    status: OrderStatus
    total_price: float
    delivery_address: Optional[str]
    notes: Optional[str]
    items: List[OrderItemOut]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────────
# Reminder
# ─────────────────────────────────────────────────────────────

class ReminderCreate(BaseModel):
    medicine_name: str = Field(min_length=1, max_length=200)
    dosage: str = Field(min_length=1, max_length=100)
    frequency: ReminderFrequency
    times: List[str] = Field(min_length=1)   # ["08:00", "20:00"]
    start_date: datetime
    end_date: Optional[datetime] = None

    @field_validator("times")
    @classmethod
    def validate_times(cls, v: List[str]) -> List[str]:
        import re
        pattern = re.compile(r"^\d{2}:\d{2}$")
        for t in v:
            if not pattern.match(t):
                raise ValueError(f"Invalid time format: {t}. Use HH:MM")
        return v


class ReminderOut(BaseModel):
    id: str
    user_id: str
    medicine_name: str
    dosage: str
    frequency: ReminderFrequency
    times_json: str
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────────
# AI Chat
# ─────────────────────────────────────────────────────────────

class AIChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: Optional[str] = None   # None = start new session


class AIChatMessageOut(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AIChatResponse(BaseModel):
    session_id: str
    reply: str
    disclaimer: str
    messages: List[AIChatMessageOut]
