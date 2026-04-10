"""
MedLinka — Main Application
FastAPI entry point: registers routers, middleware, lifecycle events
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.database import init_db
from app.services.notification_service import scheduler
from app.routers import (
    auth_router,
    users_router,
    doctors_router,
    appointments_router,
    pharmacy_router,
    orders_router,
    reminders_router,
    ai_chat_router,
)

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
)
logger = logging.getLogger("medlinka")


# ── Lifespan (startup / shutdown) ─────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──
    logger.info("🚀 MedLinka backend starting...")
    await init_db()
    logger.info("✅ Database tables created / verified")

    scheduler.start()
    logger.info("✅ Reminder scheduler started")

    yield

    # ── Shutdown ──
    scheduler.shutdown(wait=False)
    logger.info("🛑 MedLinka backend stopped")


# ── App instance ──────────────────────────────────────────────

app = FastAPI(
    title="MedLinka API",
    description=(
        "Healthcare platform API — Telemedicine · Pharmacy · AI Symptom Analysis\n\n"
        "Supports: 🇸🇦 Arabic · 🇹🇷 Turkish · 🇬🇧 English\n\n"
        "Pass `Accept-Language: ar | tr | en` header to receive responses in your language."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── CORS ──────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global exception handlers ─────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return clean validation errors with field names."""
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({"field": field, "message": error["msg"]})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# ── Routes ────────────────────────────────────────────────────

API_PREFIX = "/api/v1"

app.include_router(auth_router,         prefix=API_PREFIX)
app.include_router(users_router,        prefix=API_PREFIX)
app.include_router(doctors_router,      prefix=API_PREFIX)
app.include_router(appointments_router, prefix=API_PREFIX)
app.include_router(pharmacy_router,     prefix=API_PREFIX)
app.include_router(orders_router,       prefix=API_PREFIX)
app.include_router(reminders_router,    prefix=API_PREFIX)
app.include_router(ai_chat_router,      prefix=API_PREFIX)


# ── Health check ──────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "supported_languages": settings.supported_languages_list,
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "message": "MedLinka API is running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }
