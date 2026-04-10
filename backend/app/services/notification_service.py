"""
MedLinka — Notification Service
Expo Push Notifications + APScheduler for medication reminders
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.i18n import t

logger = logging.getLogger(__name__)

# Global scheduler instance (started in main.py)
scheduler = AsyncIOScheduler(timezone="UTC")


# ── Single push notification ──────────────────────────────────

async def send_push_notification(
    token: str,
    title: str,
    body: str,
    data: Optional[dict] = None,
) -> bool:
    """
    Send a single Expo push notification.
    Returns True on success, False on failure.
    """
    if not token or not token.startswith("ExponentPushToken["):
        logger.warning(f"Invalid or missing Expo push token: {token}")
        return False

    try:
        response = PushClient().publish(
            PushMessage(
                to=token,
                title=title,
                body=body,
                data=data or {},
                sound="default",
                badge=1,
            )
        )
        response.validate_response()
        logger.info(f"Push notification sent successfully to {token[:30]}...")
        return True

    except DeviceNotRegisteredError:
        logger.warning(f"Device not registered: {token[:30]}...")
        return False
    except (PushServerError, PushTicketError) as e:
        logger.error(f"Push notification failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected push error: {e}")
        return False


# ── Reminder scheduler ────────────────────────────────────────

async def _fire_reminder(token: str, medicine_name: str, dosage: str, lang: str) -> None:
    """Callback executed by APScheduler at reminder time."""
    title = t("reminder.notification_title", lang=lang)
    body = t("reminder.notification_body", lang=lang, medicine_name=medicine_name, dosage=dosage)
    await send_push_notification(token=token, title=title, body=body)


async def schedule_reminder_notifications(token: str, reminder, lang: str = "ar") -> None:
    """
    Register APScheduler jobs for a reminder.
    Supports: once, daily, twice_daily, three_times_daily, weekly
    """
    times: list[str] = json.loads(reminder.times_json)
    end_date = reminder.end_date

    for time_str in times:
        hour, minute = map(int, time_str.split(":"))
        job_id = f"reminder_{reminder.id}_{time_str.replace(':', '')}"

        # Remove existing job if any
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)

        kwargs = dict(
            func=_fire_reminder,
            kwargs={
                "token": token,
                "medicine_name": reminder.medicine_name,
                "dosage": reminder.dosage,
                "lang": lang,
            },
            id=job_id,
            replace_existing=True,
        )

        freq = reminder.frequency.value

        if freq == "once":
            run_date = reminder.start_date.replace(hour=hour, minute=minute, second=0)
            scheduler.add_job(trigger="date", run_date=run_date, **kwargs)

        elif freq == "daily":
            scheduler.add_job(
                trigger=CronTrigger(hour=hour, minute=minute, start_date=reminder.start_date, end_date=end_date),
                **kwargs,
            )

        elif freq == "twice_daily":
            scheduler.add_job(
                trigger=CronTrigger(hour=hour, minute=minute, start_date=reminder.start_date, end_date=end_date),
                **kwargs,
            )

        elif freq == "three_times_daily":
            scheduler.add_job(
                trigger=CronTrigger(hour=hour, minute=minute, start_date=reminder.start_date, end_date=end_date),
                **kwargs,
            )

        elif freq == "weekly":
            scheduler.add_job(
                trigger=CronTrigger(
                    day_of_week=reminder.start_date.strftime("%a").lower()[:3],
                    hour=hour,
                    minute=minute,
                    start_date=reminder.start_date,
                    end_date=end_date,
                ),
                **kwargs,
            )

        logger.info(f"Scheduled reminder job: {job_id} at {time_str} ({freq})")


def remove_reminder_jobs(reminder_id: str) -> None:
    """Remove all scheduler jobs for a given reminder."""
    for job in scheduler.get_jobs():
        if job.id.startswith(f"reminder_{reminder_id}_"):
            scheduler.remove_job(job.id)
            logger.info(f"Removed reminder job: {job.id}")
