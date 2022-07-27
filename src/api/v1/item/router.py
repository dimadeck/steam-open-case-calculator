from typing import List, Union, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from api.middleware.user import get_current_user
from api.v1.item.crud import CrudItem, get_crud_item
from api.v1.item.schema import ItemModel, ItemModelBase
from api.v1.open_case.crud import get_crud_open_case, CrudOpenCase
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
        db: CrudItem = Depends(get_crud_item),
        current_user: UserModel = Depends(get_current_user),
):
    return await db.create_item(
        open_case_uuid=data.open_case_uuid,
        profile_id=current_user.profile_id,
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
        open_case_uuid: Optional[Union[str, UUID]] = None,
        is_shown: bool = False,
        db: CrudItem = Depends(get_crud_item),
        current_user: UserModel = Depends(get_current_user)
):
    return await db.get_items(profile_id=current_user.profile_id, open_case_uuid=open_case_uuid, is_shown=is_shown)


@router.post(
    '/item/{asset_id}/replace',
    response_model=ItemModel,
    summary='Перенести Item в другой OpenCase'
)
async def replace_item(
        asset_id: int,
        open_case_uuid: Union[str, UUID],
        current_user: UserModel = Depends(get_current_user),
        db: CrudItem = Depends(get_crud_item),
        crud_open_case: CrudOpenCase = Depends(get_crud_open_case)
):
    await crud_open_case.get_open_case_by_uuid(profile_id=current_user.profile_id, open_case_uuid=open_case_uuid)
    return await db.update_item(profile_id=current_user.profile_id, asset_id=asset_id, open_case_uuid=open_case_uuid)


@router.post(
    '/item/{asset_id}/show',
    response_model=ItemModel,
    summary='Пометить Item как просмотренный'
)
async def replace_item(
        asset_id: int,
        current_user: UserModel = Depends(get_current_user),
        db: CrudItem = Depends(get_crud_item)
):
    return await db.update_item(profile_id=current_user.profile_id, asset_id=asset_id, is_shown=True)
