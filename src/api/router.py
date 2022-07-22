from fastapi import APIRouter
from api.v1.test import router as test_router
from api.v1.item.router import router as item_router
router = APIRouter()


router.include_router(test_router)
router.include_router(item_router)