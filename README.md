# MedLinka 🏥

Healthcare platform — Telemedicine · Pharmacy · AI Symptom Analysis

**Stack:** Python FastAPI · React Native (Expo) · React Dashboard  
**Languages:** 🇸🇦 Arabic (RTL) · 🇹🇷 Turkish · 🇬🇧 English

---

## Project Structure

```
medlinka/
├── backend/      → FastAPI + SQLite (Python)
├── mobile/       → React Native + Expo (iOS + Android)
├── dashboard/    → React + Vite (Web)
└── docker-compose.yml
```

---

## Quick Start (Manual)

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY in .env
python main.py
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### 2. Seed demo data
```bash
cd backend
python seed.py
```

### 3. Mobile App
```bash
cd mobile
npm install
npx expo start
# Scan QR with Expo Go app on your phone
```

### 4. Web Dashboard
```bash
cd dashboard
npm install
npm run dev
# → http://localhost:3000
```

---

## Quick Start (Docker)
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add GEMINI_API_KEY
docker-compose up --build
```

---

## Demo Accounts (after seeding)

| Role     | Email                    | Password  | Language |
|----------|--------------------------|-----------|----------|
| Patient  | ahmed@medlinka.com       | Test1234  | Arabic   |
| Patient  | mehmet@medlinka.com      | Test1234  | Turkish  |
| Patient  | john@medlinka.com        | Test1234  | English  |
| Doctor   | dr.sarah@medlinka.com    | Test1234  | Arabic   |
| Doctor   | dr.ali@medlinka.com      | Test1234  | English  |
| Doctor   | dr.ayse@medlinka.com     | Test1234  | Turkish  |
| Pharmacy | pharmacy@medlinka.com    | Test1234  | Arabic   |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Login |
| GET  | `/api/v1/users/me` | My profile |
| GET  | `/api/v1/doctors` | List doctors |
| POST | `/api/v1/appointments` | Book appointment |
| GET  | `/api/v1/pharmacy/medicines` | Browse medicines |
| POST | `/api/v1/orders` | Place order |
| POST | `/api/v1/reminders` | Set reminder |
| POST | `/api/v1/ai/chat` | AI chat |

Full docs → http://localhost:8000/docs

---

## Multilingual

Send `Accept-Language` header: `ar` · `tr` · `en`  
All error messages, notifications, and AI responses adapt automatically.

---

## Running Tests
```bash
cd backend
pytest tests/ -v
```
