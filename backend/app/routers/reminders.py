"""
MedLinka — Reminders Router
POST   /api/v1/reminders        — create reminder
GET    /api/v1/reminders        — list my reminders
DELETE /api/v1/reminders/{id}   — delete reminder
"""

import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, Reminder
from app.schemas.schemas import ReminderCreate, ReminderOut, OKResponse
from app.utils.dependencies import get_current_user
from app.i18n import t, get_language_from_header
from app.services.notification_service import schedule_reminder_notifications

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    body: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    reminder = Reminder(
        user_id=current_user.id,
        medicine_name=body.medicine_name,
        dosage=body.dosage,
        frequency=body.frequency,
        times_json=json.dumps(body.times),
        start_date=body.start_date,
        end_date=body.end_date,
    )
    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)

    # Schedule push notifications if user has a push token
    if current_user.expo_push_token:
        await schedule_reminder_notifications(
            token=current_user.expo_push_token,
            reminder=reminder,
            lang=current_user.preferred_language.value,
        )

    return reminder


@router.get("", response_model=List[ReminderOut])
async def list_reminders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Reminder)
        .where(Reminder.user_id == current_user.id, Reminder.is_active == True)
        .order_by(Reminder.created_at.desc())
    )
    return result.scalars().all()


@router.delete("/{reminder_id}", response_model=OKResponse)
async def delete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == current_user.id)
    )
    reminder = result.scalar_one_or_none()

    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("reminder.not_found", lang))

    reminder.is_active = False
    await db.commit()
    return OKResponse(message=t("reminder.deleted", lang))
