from fastapi import APIRouter

from .secret_router import router as router_secret


router = APIRouter(prefix="/api/v1")
router.include_router(router_secret)

