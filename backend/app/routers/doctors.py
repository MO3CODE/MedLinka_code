"""
MedLinka — Doctors Router
GET  /api/v1/doctors               — list all available doctors
GET  /api/v1/doctors/{id}          — doctor details
POST /api/v1/doctors/profile       — doctor creates their profile
PUT  /api/v1/doctors/profile       — doctor updates their profile
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models import User, DoctorProfile, UserRole, DoctorSpecialty
from app.schemas.schemas import DoctorProfileCreate, DoctorProfileOut, DoctorListItem, OKResponse
from app.utils.dependencies import get_current_user, require_role
from app.i18n import t, get_language_from_header

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("", response_model=List[DoctorListItem])
async def list_doctors(
    specialty: Optional[DoctorSpecialty] = Query(default=None),
    available_only: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
):
    conditions = []
    if available_only:
        conditions.append(DoctorProfile.is_available == True)
    if specialty:
        conditions.append(DoctorProfile.specialty == specialty)

    result = await db.execute(
        select(DoctorProfile).where(and_(*conditions)).order_by(DoctorProfile.rating.desc())
    )
    return result.scalars().all()


@router.get("/{doctor_id}", response_model=DoctorProfileOut)
async def get_doctor(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(DoctorProfile).where(DoctorProfile.id == doctor_id))
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("doctor.not_found", lang))
    return doctor


@router.post("/profile", response_model=DoctorProfileOut, status_code=status.HTTP_201_CREATED)
async def create_doctor_profile(
    body: DoctorProfileCreate,
    current_user: User = Depends(require_role(UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    existing = await db.execute(select(DoctorProfile).where(DoctorProfile.user_id == current_user.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")

    profile = DoctorProfile(user_id=current_user.id, **body.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.put("/profile", response_model=DoctorProfileOut)
async def update_doctor_profile(
    body: DoctorProfileCreate,
    current_user: User = Depends(require_role(UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    result = await db.execute(select(DoctorProfile).where(DoctorProfile.user_id == current_user.id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("doctor.not_found", lang))

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)
    return profile
