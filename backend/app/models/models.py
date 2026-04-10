"""
MedLinka — Database Models
All tables defined here using SQLAlchemy 2.0 ORM
"""

import enum
import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    String, Boolean, Float, Integer, Text,
    ForeignKey, DateTime, Enum as SAEnum, JSON,
    UniqueConstraint, Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ─────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    PATIENT   = "patient"
    DOCTOR    = "doctor"
    PHARMACY  = "pharmacy"
    ADMIN     = "admin"


class Language(str, enum.Enum):
    AR = "ar"
    TR = "tr"
    EN = "en"


class AppointmentStatus(str, enum.Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class AppointmentType(str, enum.Enum):
    CHAT  = "chat"
    VIDEO = "video"


class OrderStatus(str, enum.Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    SHIPPED   = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ReminderFrequency(str, enum.Enum):
    ONCE      = "once"
    DAILY     = "daily"
    TWICE_DAY = "twice_daily"
    THREE_DAY = "three_times_daily"
    WEEKLY    = "weekly"


class DoctorSpecialty(str, enum.Enum):
    GENERAL       = "general"
    CARDIOLOGY    = "cardiology"
    DERMATOLOGY   = "dermatology"
    NEUROLOGY     = "neurology"
    ORTHOPEDICS   = "orthopedics"
    PEDIATRICS    = "pediatrics"
    PSYCHIATRY    = "psychiatry"
    GYNECOLOGY    = "gynecology"
    OPHTHALMOLOGY = "ophthalmology"
    ENT           = "ent"
    DENTISTRY     = "dentistry"
    OTHER         = "other"


# ─────────────────────────────────────────────────────────────
# User
# ─────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.PATIENT, nullable=False)
    preferred_language: Mapped[Language] = mapped_column(SAEnum(Language), default=Language.AR, nullable=False)
    expo_push_token: Mapped[Optional[str]] = mapped_column(String(200))   # for mobile notifications
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    doctor_profile: Mapped[Optional["DoctorProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    pharmacy_profile: Mapped[Optional["PharmacyProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    appointments_as_patient: Mapped[List["Appointment"]] = relationship(foreign_keys="[Appointment.patient_id]", back_populates="patient")
    orders: Mapped[List["Order"]] = relationship(back_populates="patient")
    reminders: Mapped[List["Reminder"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    chat_sessions: Mapped[List["AIChatSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")


# ─────────────────────────────────────────────────────────────
# Refresh Token
# ─────────────────────────────────────────────────────────────

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")


# ─────────────────────────────────────────────────────────────
# Doctor Profile
# ─────────────────────────────────────────────────────────────

class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    specialty: Mapped[DoctorSpecialty] = mapped_column(SAEnum(DoctorSpecialty), default=DoctorSpecialty.GENERAL)
    bio_ar: Mapped[Optional[str]] = mapped_column(Text)
    bio_tr: Mapped[Optional[str]] = mapped_column(Text)
    bio_en: Mapped[Optional[str]] = mapped_column(Text)
    years_experience: Mapped[int] = mapped_column(Integer, default=0)
    consultation_fee: Mapped[float] = mapped_column(Float, default=0.0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    available_days: Mapped[Optional[str]] = mapped_column(String(50))  # e.g. "mon,tue,wed"
    available_from: Mapped[Optional[str]] = mapped_column(String(5))   # e.g. "09:00"
    available_to: Mapped[Optional[str]] = mapped_column(String(5))     # e.g. "17:00"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="doctor_profile")
    appointments: Mapped[List["Appointment"]] = relationship(foreign_keys="[Appointment.doctor_id]", back_populates="doctor")


# ─────────────────────────────────────────────────────────────
# Pharmacy Profile
# ─────────────────────────────────────────────────────────────

class PharmacyProfile(Base):
    __tablename__ = "pharmacy_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    pharmacy_name_ar: Mapped[str] = mapped_column(String(200), nullable=False)
    pharmacy_name_tr: Mapped[Optional[str]] = mapped_column(String(200))
    pharmacy_name_en: Mapped[Optional[str]] = mapped_column(String(200))
    address: Mapped[Optional[str]] = mapped_column(Text)
    license_number: Mapped[Optional[str]] = mapped_column(String(100))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="pharmacy_profile")
    medicines: Mapped[List["Medicine"]] = relationship(back_populates="pharmacy", cascade="all, delete-orphan")


# ─────────────────────────────────────────────────────────────
# Medicine
# ─────────────────────────────────────────────────────────────

class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pharmacy_id: Mapped[str] = mapped_column(ForeignKey("pharmacy_profiles.id", ondelete="CASCADE"), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(200), nullable=False)
    name_tr: Mapped[Optional[str]] = mapped_column(String(200))
    name_en: Mapped[Optional[str]] = mapped_column(String(200))
    description_ar: Mapped[Optional[str]] = mapped_column(Text)
    description_tr: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    requires_prescription: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pharmacy: Mapped["PharmacyProfile"] = relationship(back_populates="medicines")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="medicine")

    __table_args__ = (
        Index("idx_medicine_pharmacy", "pharmacy_id"),
        Index("idx_medicine_category", "category"),
    )


# ─────────────────────────────────────────────────────────────
# Appointment
# ─────────────────────────────────────────────────────────────

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_id: Mapped[str] = mapped_column(ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    type: Mapped[AppointmentType] = mapped_column(SAEnum(AppointmentType), default=AppointmentType.CHAT)
    status: Mapped[AppointmentStatus] = mapped_column(SAEnum(AppointmentStatus), default=AppointmentStatus.PENDING)
    notes_by_patient: Mapped[Optional[str]] = mapped_column(Text)
    notes_by_doctor: Mapped[Optional[str]] = mapped_column(Text)
    prescription_id: Mapped[Optional[str]] = mapped_column(ForeignKey("prescriptions.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient: Mapped["User"] = relationship(foreign_keys=[patient_id], back_populates="appointments_as_patient")
    doctor: Mapped["DoctorProfile"] = relationship(foreign_keys=[doctor_id], back_populates="appointments")
    prescription: Mapped[Optional["Prescription"]] = relationship(back_populates="appointment")

    __table_args__ = (
        UniqueConstraint("doctor_id", "scheduled_at", name="uq_doctor_slot"),
        Index("idx_appointment_patient", "patient_id"),
        Index("idx_appointment_doctor", "doctor_id"),
        Index("idx_appointment_status", "status"),
    )


# ─────────────────────────────────────────────────────────────
# Prescription
# ─────────────────────────────────────────────────────────────

class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_id: Mapped[str] = mapped_column(ForeignKey("doctor_profiles.id"), nullable=False)
    medicines_json: Mapped[Optional[str]] = mapped_column(Text)  # JSON list of {name, dosage, frequency}
    notes: Mapped[Optional[str]] = mapped_column(Text)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    appointment: Mapped[Optional["Appointment"]] = relationship(back_populates="prescription")


# ─────────────────────────────────────────────────────────────
# Order
# ─────────────────────────────────────────────────────────────

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    total_price: Mapped[float] = mapped_column(Float, default=0.0)
    delivery_address: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_order_patient", "patient_id"),
        Index("idx_order_status", "status"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    medicine_id: Mapped[str] = mapped_column(ForeignKey("medicines.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    medicine: Mapped["Medicine"] = relationship(back_populates="order_items")


# ─────────────────────────────────────────────────────────────
# Reminder
# ─────────────────────────────────────────────────────────────

class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    medicine_name: Mapped[str] = mapped_column(String(200), nullable=False)
    dosage: Mapped[str] = mapped_column(String(100), nullable=False)
    frequency: Mapped[ReminderFrequency] = mapped_column(SAEnum(ReminderFrequency), nullable=False)
    times_json: Mapped[str] = mapped_column(Text, nullable=False)   # JSON: ["08:00", "20:00"]
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="reminders")


# ─────────────────────────────────────────────────────────────
# AI Chat Session
# ─────────────────────────────────────────────────────────────

class AIChatSession(Base):
    __tablename__ = "ai_chat_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language: Mapped[Language] = mapped_column(SAEnum(Language), default=Language.AR)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="chat_sessions")
    messages: Mapped[List["AIChatMessage"]] = relationship(back_populates="session", cascade="all, delete-orphan", order_by="AIChatMessage.created_at")


class AIChatMessage(Base):
    __tablename__ = "ai_chat_messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(ForeignKey("ai_chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)   # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["AIChatSession"] = relationship(back_populates="messages")
