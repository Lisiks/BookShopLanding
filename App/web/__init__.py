from fastapi import APIRouter

from .admin_routes import router as admin_router
from .users_routes import router as users_router
from .healthcheck import router as health_router
from .jahnres_routes import router as jahnres_router
from .authors_routes import router as authors_router
from .shops_routes import router as shops_router

router = APIRouter()


router.include_router(jahnres_router)
router.include_router(authors_router)
router.include_router(shops_router)

router.include_router(admin_router)
router.include_router(users_router)
router.include_router(health_router)