# MedLinka — Backend API

Healthcare platform backend built with **FastAPI** + **SQLite** + **Python 3.11+**

---

## Quick Start

### 1. Prerequisites
- Python 3.11+
- pip

### 2. Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run the server
```bash
python main.py
```
Server starts at → **http://localhost:8000**

### 4. Seed sample data (optional)
```bash
python seed.py
```

### 5. API Documentation
- Swagger UI → http://localhost:8000/docs
- ReDoc      → http://localhost:8000/redoc
- Health     → http://localhost:8000/health

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh token |
| POST | `/api/v1/auth/logout` | Logout |
| GET | `/api/v1/users/me` | My profile |
| PUT | `/api/v1/users/me` | Update profile |
| GET | `/api/v1/doctors` | List doctors |
| GET | `/api/v1/doctors/{id}` | Doctor details |
| POST | `/api/v1/appointments` | Book appointment |
| GET | `/api/v1/appointments` | My appointments |
| DELETE | `/api/v1/appointments/{id}` | Cancel appointment |
| GET | `/api/v1/pharmacy/medicines` | Browse medicines |
| POST | `/api/v1/orders` | Place order |
| GET | `/api/v1/orders` | My orders |
| POST | `/api/v1/reminders` | Set reminder |
| GET | `/api/v1/reminders` | My reminders |
| POST | `/api/v1/ai/chat` | AI symptom chat |

---

## Multilingual Support

Send `Accept-Language` header with every request:

```
Accept-Language: ar   → Arabic  (العربية)
Accept-Language: tr   → Turkish (Türkçe)
Accept-Language: en   → English
```

All error messages, notifications, and AI responses adapt to the requested language.

---

## Test Accounts (after seeding)

| Role | Email | Password |
|------|-------|----------|
| Patient (AR) | ahmed@medlinka.com | Test1234 |
| Patient (TR) | mehmet@medlinka.com | Test1234 |
| Patient (EN) | john@medlinka.com | Test1234 |
| Doctor | dr.sarah@medlinka.com | Test1234 |
| Doctor | dr.ali@medlinka.com | Test1234 |
| Doctor | dr.ayse@medlinka.com | Test1234 |
| Pharmacy | pharmacy@medlinka.com | Test1234 |

---

## Running Tests
```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```
