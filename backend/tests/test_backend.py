"""
MedLinka — Backend Tests
Run: pytest tests/ -v
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.database import Base, get_db

# ── In-memory test database ───────────────────────────────────
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestSession() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


# ── Auth Tests ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_register_patient(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "test@medlinka.com",
        "password": "Test1234",
        "full_name": "Test User",
        "role": "patient",
        "preferred_language": "ar",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "dup@medlinka.com",
        "password": "Test1234",
        "full_name": "Dup User",
        "role": "patient",
        "preferred_language": "en",
    }
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "email": "login@medlinka.com",
        "password": "Test1234",
        "full_name": "Login User",
        "role": "patient",
        "preferred_language": "tr",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@medlinka.com",
        "password": "Test1234",
    })
    assert resp.status_code == 200
    assert resp.json()["access_token"]


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/api/v1/auth/register", json={
        "email": "wp@medlinka.com",
        "password": "Test1234",
        "full_name": "WP User",
        "role": "patient",
        "preferred_language": "en",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "wp@medlinka.com",
        "password": "WrongPass9",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_profile(client):
    reg = await client.post("/api/v1/auth/register", json={
        "email": "profile@medlinka.com",
        "password": "Test1234",
        "full_name": "Profile User",
        "role": "patient",
        "preferred_language": "ar",
    })
    token = reg.json()["access_token"]
    resp = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "profile@medlinka.com"


@pytest.mark.asyncio
async def test_i18n_error_arabic(client):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "none@x.com", "password": "Bad1234"},
        headers={"Accept-Language": "ar"},
    )
    assert resp.status_code == 401
    assert "غير صحيحة" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_i18n_error_turkish(client):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "none@x.com", "password": "Bad1234"},
        headers={"Accept-Language": "tr"},
    )
    assert resp.status_code == 401
    assert "Geçersiz" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "ar" in data["supported_languages"]
    assert "tr" in data["supported_languages"]
    assert "en" in data["supported_languages"]
