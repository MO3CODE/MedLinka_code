"""
MedLinka — Auth Dependencies
FastAPI dependencies for extracting and validating the current user
"""

from typing import Optional
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, UserRole
from app.utils.security import decode_token
from app.i18n import t, get_language_from_header

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
) -> User:
    lang = get_language_from_header(accept_language)
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=t("auth.unauthorized", lang))

    user_id: str = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=t("auth.unauthorized", lang))

    return user


async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def require_role(*roles: UserRole):
    async def checker(
        user: User = Depends(get_current_user),
        accept_language: Optional[str] = Header(default=None),
    ) -> User:
        lang = get_language_from_header(accept_language)
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=t("auth.forbidden", lang))
        return user
    return checker
