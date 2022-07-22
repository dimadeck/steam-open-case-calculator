from fastapi import APIRouter

from core.last_item_info import LastItemInfo

router = APIRouter()


@router.get(
    "/test",
    summary="Тестовый маршрут"
)
def test(profile_id: int):
    return LastItemInfo(profile_id).get_item_info()