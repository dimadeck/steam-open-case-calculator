from typing import List

from fastapi import APIRouter, Depends

from api.middleware.user import get_current_user
from api.v1.item.crud import CrudItem, get_crud_item
from api.v1.item.schema import ItemModel, ItemModelBase
from api.v1.user.schema import UserModel

router = APIRouter()


@router.post(
    "/item",
    status_code=201,
    response_model=ItemModel,
    summary="Добавить новый дроп"
)
async def create_item(
        data: ItemModelBase,
        db: CrudItem = Depends(get_crud_item)
):
    return await db.create_item(
        profile_id=data.profile_id,
        asset_id=data.asset_id,
        class_id=data.class_id,
        instance_id=data.instance_id,
        name=data.name,
        item_type=data.item_type,
        weapon=data.weapon,
        exterior=data.exterior,
        rarity=data.rarity,
        rarity_color=data.rarity_color,
        image_url=data.image_url,
        price=data.price,
        item_float=data.item_float
    )


@router.get(
    '/item',
    response_model=List[ItemModel],
    summary='Получить все предметы'
)
async def get_item(
        db: CrudItem = Depends(get_crud_item),
        current_user: UserModel = Depends(get_current_user)
):
    print(current_user)
    return await db.get_items()


@router.get(
    '/show_items',
    response_model=List[ItemModel],
    summary='Получить непросмотренные предметы'
)
async def get_item(
        profile_id: int,
        db: CrudItem = Depends(get_crud_item)
):
    return await db.show_items(profile_id)
