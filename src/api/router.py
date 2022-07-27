from fastapi import APIRouter
from api.v1.item.router import router as item_router
from api.v1.user.router import router as steam_auth_router
from api.v1.open_case.router import router as open_case_router
router = APIRouter()


router.include_router(item_router)
router.include_router(steam_auth_router)
router.include_router(open_case_router)