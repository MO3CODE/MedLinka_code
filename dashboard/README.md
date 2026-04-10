# MedLinka — Web Dashboard

React + Vite + TypeScript — runs in any browser

---

## Quick Start

```bash
cd dashboard
npm install
npm run dev
```

Dashboard opens at → **http://localhost:3000**

> Make sure the backend is running on port 8000 first.

---

## Pages by Role

### Admin
| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Stats, charts, recent appointments |
| Doctors | `/doctors` | List all doctors + specialty breakdown |
| Appointments | `/appointments` | All appointments with status filters |
| Medicines | `/pharmacy` | Browse pharmacy inventory |
| Orders | `/orders` | All orders with status filters |

### Doctor
| Page | URL | Description |
|------|-----|-------------|
| My Schedule | `/` | Upcoming appointments |
| Notes | (inline) | Add notes + update appointment status |

### Pharmacy
| Page | URL | Description |
|------|-----|-------------|
| Medicines | `/` | Manage medicine inventory |
| Add Medicine | (modal) | Add new medicine (AR/TR/EN names) |
| Orders | `/orders` | View incoming orders |

---

## Language Switcher
Click **ع / TR / EN** in the top bar — the UI instantly switches language and RTL/LTR direction.

---

## Demo Accounts
| Role | Email | Password |
|------|-------|----------|
| Admin/Patient | ahmed@medlinka.com | Test1234 |
| Doctor | dr.sarah@medlinka.com | Test1234 |
| Pharmacy | pharmacy@medlinka.com | Test1234 |
