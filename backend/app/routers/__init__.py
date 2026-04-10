from .auth import router as auth_router
from .users import router as users_router
from .doctors import router as doctors_router
from .appointments import router as appointments_router
from .pharmacy import router as pharmacy_router
from .orders import router as orders_router
from .reminders import router as reminders_router
from .ai_chat import router as ai_chat_router

__all__ = [
    "auth_router",
    "users_router",
    "doctors_router",
    "appointments_router",
    "pharmacy_router",
    "orders_router",
    "reminders_router",
    "ai_chat_router",
]
