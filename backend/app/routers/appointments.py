"""
MedLinka — Appointments Router
POST /api/v1/appointments                    — patient books
GET  /api/v1/appointments                    — patient's appointments
GET  /api/v1/appointments/{id}               — single appointment
DELETE /api/v1/appointments/{id}             — patient cancels
PUT  /api/v1/appointments/{id}/doctor-notes  — doctor adds notes
GET  /api/v1/appointments/doctor/schedule    — doctor's schedule
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models import User, Appointment, DoctorProfile, UserRole, AppointmentStatus
from app.schemas.schemas import AppointmentCreate, AppointmentOut, DoctorNoteUpdate, OKResponse
from app.utils.dependencies import get_current_user, require_role
from app.i18n import t, get_language_from_header
from app.services.notification_service import send_push_notification

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
async def book_appointment(
    body: AppointmentCreate,
    current_user: User = Depends(require_role(UserRole.PATIENT)),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    # Verify doctor exists
    result = await db.execute(select(DoctorProfile).where(DoctorProfile.id == body.doctor_id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("doctor.not_found", lang))

    if not doctor.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=t("doctor.unavailable", lang))

    # Check slot not taken
    slot_check = await db.execute(
        select(Appointment).where(
            and_(
                Appointment.doctor_id == body.doctor_id,
                Appointment.scheduled_at == body.scheduled_at,
                Appointment.status.notin_([AppointmentStatus.CANCELLED]),
            )
        )
    )
    if slot_check.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=t("appointment.slot_taken", lang))

    appointment = Appointment(
        patient_id=current_user.id,
        doctor_id=body.doctor_id,
        scheduled_at=body.scheduled_at,
        duration_minutes=body.duration_minutes,
        type=body.type,
        notes_by_patient=body.notes_by_patient,
        status=AppointmentStatus.PENDING,
    )
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)

    # Notify the doctor
    if doctor.user and doctor.user.expo_push_token:
        await send_push_notification(
            token=doctor.user.expo_push_token,
            title=t("appointment.reminder_set", lang=doctor.user.preferred_language.value),
            body=f"{current_user.full_name} — {body.scheduled_at.strftime('%Y-%m-%d %H:%M')}",
        )

    return appointment


@router.get("", response_model=List[AppointmentOut])
async def list_my_appointments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Appointment)
        .where(Appointment.patient_id == current_user.id)
        .order_by(Appointment.scheduled_at.desc())
    )
    return result.scalars().all()


@router.get("/doctor/schedule", response_model=List[AppointmentOut])
async def doctor_schedule(
    current_user: User = Depends(require_role(UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db),
):
    profile_result = await db.execute(select(DoctorProfile).where(DoctorProfile.user_id == current_user.id))
    profile = profile_result.scalar_one_or_none()
    if not profile:
        return []

    result = await db.execute(
        select(Appointment)
        .where(
            and_(
                Appointment.doctor_id == profile.id,
                Appointment.scheduled_at >= datetime.utcnow(),
            )
        )
        .order_by(Appointment.scheduled_at)
    )
    return result.scalars().all()


@router.get("/{appointment_id}", response_model=AppointmentOut)
async def get_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appt = result.scalar_one_or_none()

    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("appointment.not_found", lang))
    return appt


@router.delete("/{appointment_id}", response_model=OKResponse)
async def cancel_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appt = result.scalar_one_or_none()

    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("appointment.not_found", lang))

    if appt.scheduled_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=t("appointment.cannot_cancel_past", lang))

    appt.status = AppointmentStatus.CANCELLED
    await db.commit()
    return OKResponse(message=t("appointment.cancelled", lang))


@router.put("/{appointment_id}/doctor-notes", response_model=AppointmentOut)
async def add_doctor_notes(
    appointment_id: str,
    body: DoctorNoteUpdate,
    current_user: User = Depends(require_role(UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appt = result.scalar_one_or_none()

    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("appointment.not_found", lang))

    appt.notes_by_doctor = body.notes_by_doctor
    if body.status:
        appt.status = body.status

    await db.commit()
    await db.refresh(appt)
    return appt
