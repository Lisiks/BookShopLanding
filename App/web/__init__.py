from fastapi import APIRouter

from .admin_routes import router as admin_router
from .users_routes import router as users_router

router = APIRouter()
router.include_router(admin_router)
router.include_router(users_router)

__all__ = [
    "admin_router",
    "users_router",
    "router"
]