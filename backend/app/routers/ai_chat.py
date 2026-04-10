"""
MedLinka — AI Chat Router
POST /api/v1/ai/chat              — send message, get AI response
GET  /api/v1/ai/sessions          — list user's chat sessions
GET  /api/v1/ai/sessions/{id}     — get full session with messages
DELETE /api/v1/ai/sessions/{id}   — delete session
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, AIChatSession, AIChatMessage, Language
from app.schemas.schemas import AIChatRequest, AIChatResponse, AIChatMessageOut, OKResponse
from app.utils.dependencies import get_current_user
from app.i18n import t, get_language_from_header
from app.services.ai_service import get_ai_response

router = APIRouter(prefix="/ai", tags=["AI Chat"])


@router.post("/chat", response_model=AIChatResponse)
async def chat(
    body: AIChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)

    # Get or create session
    if body.session_id:
        result = await db.execute(
            select(AIChatSession).where(
                AIChatSession.id == body.session_id,
                AIChatSession.user_id == current_user.id,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail=t("general.not_found", lang))
    else:
        session = AIChatSession(
            user_id=current_user.id,
            language=Language(lang),
        )
        db.add(session)
        await db.flush()

    # Load conversation history for context
    history_result = await db.execute(
        select(AIChatMessage)
        .where(AIChatMessage.session_id == session.id)
        .order_by(AIChatMessage.created_at)
    )
    history = history_result.scalars().all()

    # Save user message
    user_msg = AIChatMessage(session_id=session.id, role="user", content=body.message)
    db.add(user_msg)
    await db.flush()

    # Call Gemini
    try:
        ai_reply = await get_ai_response(
            user_message=body.message,
            history=history,
            lang=lang,
        )
    except Exception:
        raise HTTPException(status_code=503, detail=t("ai.error", lang))

    # Save AI response
    ai_msg = AIChatMessage(session_id=session.id, role="assistant", content=ai_reply)
    db.add(ai_msg)
    await db.commit()

    # Return updated messages
    all_msgs_result = await db.execute(
        select(AIChatMessage).where(AIChatMessage.session_id == session.id).order_by(AIChatMessage.created_at)
    )
    all_msgs = all_msgs_result.scalars().all()

    return AIChatResponse(
        session_id=session.id,
        reply=ai_reply,
        disclaimer=t("ai.disclaimer", lang),
        messages=[AIChatMessageOut.model_validate(m) for m in all_msgs],
    )


@router.get("/sessions", response_model=List[dict])
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AIChatSession)
        .where(AIChatSession.user_id == current_user.id)
        .order_by(AIChatSession.created_at.desc())
    )
    sessions = result.scalars().all()
    return [{"id": s.id, "language": s.language, "created_at": s.created_at} for s in sessions]


@router.get("/sessions/{session_id}", response_model=AIChatResponse)
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(
        select(AIChatSession).where(
            AIChatSession.id == session_id,
            AIChatSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail=t("general.not_found", lang))

    msgs_result = await db.execute(
        select(AIChatMessage).where(AIChatMessage.session_id == session.id).order_by(AIChatMessage.created_at)
    )
    msgs = msgs_result.scalars().all()

    return AIChatResponse(
        session_id=session.id,
        reply=msgs[-1].content if msgs else "",
        disclaimer=t("ai.disclaimer", lang),
        messages=[AIChatMessageOut.model_validate(m) for m in msgs],
    )


@router.delete("/sessions/{session_id}", response_model=OKResponse)
async def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(
        select(AIChatSession).where(
            AIChatSession.id == session_id,
            AIChatSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail=t("general.not_found", lang))

    await db.delete(session)
    await db.commit()
    return OKResponse(message=t("general.success", lang))
