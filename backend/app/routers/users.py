"""
MedLinka — Users Router
GET  /api/v1/users/me
PUT  /api/v1/users/me
POST /api/v1/users/me/change-password
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas.schemas import UserOut, UpdateProfileRequest, ChangePasswordRequest, OKResponse
from app.utils.dependencies import get_current_user
from app.utils.security import verify_password, hash_password
from app.i18n import t, get_language_from_header

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
async def update_profile(
    body: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post("/me/change-password", response_model=OKResponse)
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=t("user.wrong_password", lang))

    current_user.hashed_password = hash_password(body.new_password)
    await db.commit()

    return OKResponse(message=t("user.password_changed", lang))
