#!/bin/bash
# ── MedLinka Startup Script ──────────────────────────────────────
# Starts both backend (FastAPI) and frontend (Vite) servers

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
DASHBOARD_DIR="$ROOT_DIR/dashboard"

echo "=================================="
echo "   MedLinka - Healthcare Platform "
echo "=================================="

# ── Backend ──────────────────────────────────────────────────────
echo ""
echo "[1/2] Starting Backend (FastAPI)..."

cd "$BACKEND_DIR"

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "  Creating Python virtual environment..."
    python3 -m venv venv
fi

# Install dependencies if needed
if ! venv/bin/python -c "import fastapi" 2>/dev/null; then
    echo "  Installing Python dependencies..."
    venv/bin/pip install -r requirements.txt -q
fi

# Seed database if empty
venv/bin/python -c "
import asyncio, sys
sys.path.insert(0, '.')
from app.database import AsyncSessionLocal
from app.models import User
async def check():
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select, func
        result = await db.execute(select(func.count()).select_from(User))
        return result.scalar()
count = asyncio.run(check())
sys.exit(0 if count > 0 else 1)
" 2>/dev/null || (echo "  Seeding demo data..." && venv/bin/python seed.py > /dev/null 2>&1)

# Start backend
venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level warning &
BACKEND_PID=$!
echo "  Backend started (PID: $BACKEND_PID)"

# Wait for backend to be ready
echo -n "  Waiting for backend..."
for i in $(seq 1 10); do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo " Ready!"
        break
    fi
    sleep 1
    echo -n "."
done

# ── Frontend ──────────────────────────────────────────────────────
echo ""
echo "[2/2] Starting Frontend (Vite)..."

cd "$DASHBOARD_DIR"

# Install node modules if needed
if [ ! -d "node_modules" ]; then
    echo "  Installing Node.js dependencies..."
    npm install -q
fi

# Fix vite permissions
chmod +x node_modules/.bin/vite 2>/dev/null || true

# Start frontend
./node_modules/.bin/vite --port 3000 --host 0.0.0.0 > /tmp/vite.log 2>&1 &
FRONTEND_PID=$!
echo "  Frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to be ready
echo -n "  Waiting for frontend..."
for i in $(seq 1 10); do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo " Ready!"
        break
    fi
    sleep 1
    echo -n "."
done

# ── Summary ───────────────────────────────────────────────────────
echo ""
echo "=================================="
echo "  MedLinka is running!"
echo "----------------------------------"
echo "  Backend API:  http://localhost:8000"
echo "  API Docs:     http://localhost:8000/docs"
echo "  Dashboard:    http://localhost:3000"
echo "----------------------------------"
echo "  Demo Accounts (password: Test1234)"
echo "  Patient (AR): ahmed@medlinka.com"
echo "  Patient (EN): john@medlinka.com"
echo "  Doctor:       dr.sarah@medlinka.com"
echo "  Pharmacy:     pharmacy@medlinka.com"
echo "=================================="
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Handle shutdown
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "Done."
    exit 0
}
trap cleanup INT TERM

wait
