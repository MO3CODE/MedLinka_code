"""
MedLinka — Pharmacy Router
GET  /api/v1/pharmacy/medicines          — browse medicines (all pharmacies)
GET  /api/v1/pharmacy/medicines/{id}     — single medicine
POST /api/v1/pharmacy/medicines          — pharmacy adds medicine
PUT  /api/v1/pharmacy/medicines/{id}     — pharmacy updates medicine
"""

import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from app.database import get_db
from app.models import User, Medicine, PharmacyProfile, UserRole
from app.schemas.schemas import MedicineCreate, MedicineOut, OKResponse
from app.utils.dependencies import get_current_user, require_role
from app.i18n import t, get_language_from_header

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@router.get("/medicines", response_model=List[MedicineOut])
async def list_medicines(
    search: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    conditions = [Medicine.is_active == True, Medicine.stock_quantity > 0]

    if category:
        conditions.append(Medicine.category == category)

    if search:
        conditions.append(
            or_(
                Medicine.name_ar.ilike(f"%{search}%"),
                Medicine.name_tr.ilike(f"%{search}%"),
                Medicine.name_en.ilike(f"%{search}%"),
            )
        )

    result = await db.execute(select(Medicine).where(and_(*conditions)))
    return result.scalars().all()


@router.get("/medicines/{medicine_id}", response_model=MedicineOut)
async def get_medicine(
    medicine_id: str,
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Medicine).where(Medicine.id == medicine_id))
    med = result.scalar_one_or_none()

    if not med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("medicine.not_found", lang))
    return med


@router.post("/medicines", response_model=MedicineOut, status_code=status.HTTP_201_CREATED)
async def add_medicine(
    body: MedicineCreate,
    current_user: User = Depends(require_role(UserRole.PHARMACY)),
    db: AsyncSession = Depends(get_db),
):
    profile_result = await db.execute(select(PharmacyProfile).where(PharmacyProfile.user_id == current_user.id))
    profile = profile_result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pharmacy profile not found")

    med = Medicine(pharmacy_id=profile.id, **body.model_dump())
    db.add(med)
    await db.commit()
    await db.refresh(med)
    return med


@router.put("/medicines/{medicine_id}", response_model=MedicineOut)
async def update_medicine(
    medicine_id: str,
    body: MedicineCreate,
    current_user: User = Depends(require_role(UserRole.PHARMACY)),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Medicine).where(Medicine.id == medicine_id))
    med = result.scalar_one_or_none()

    if not med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=t("medicine.not_found", lang))

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(med, field, value)

    await db.commit()
    await db.refresh(med)
    return med
