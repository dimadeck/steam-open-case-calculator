from typing import List, Union, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from api.middleware.user import get_current_user
from api.v1.open_case.crud import CrudOpenCase, get_crud_open_case
from api.v1.open_case.schema import OpenCaseBaseModel, OpenCaseModel
from api.v1.user.schema import UserModel

router = APIRouter()


@router.post(
    "/open_case",
    status_code=201,
    response_model=OpenCaseModel,
    summary="Добавить новое открытие кейсов"
)
async def create_item(
        data: OpenCaseBaseModel,
        db: CrudOpenCase = Depends(get_crud_open_case),
        current_user: UserModel = Depends(get_current_user)
):
    return await db.create_open_case(
        profile_id=current_user.profile_id,
        name=data.name,
        description=data.description
    )


@router.get(
    '/open_case',
    response_model=Union[List[OpenCaseModel], OpenCaseModel],
    summary='Получить открытия кейсов'
)
async def get_open_case(
        open_case_uuid: Optional[Union[str, UUID]] = None,
        with_items: bool = False,
        db: CrudOpenCase = Depends(get_crud_open_case),
        current_user: UserModel = Depends(get_current_user)
):
    if open_case_uuid:
        return await db.get_open_case_by_uuid(profile_id=current_user.profile_id, open_case_uuid=open_case_uuid)
    return await db.get_open_cases(profile_id=current_user.profile_id, with_items=with_items)


@router.patch(
    '/open_case',
    response_model=OpenCaseModel,
    summary='Обновить кейс'
)
async def update_open_case(
        open_case_uuid: Union[str, UUID],
        data: OpenCaseBaseModel,
        db: CrudOpenCase = Depends(get_crud_open_case),
        current_user: UserModel = Depends(get_current_user)
):
    return await db.update_open_case(
        open_case_uuid=open_case_uuid,
        profile_id=current_user.profile_id,
        name=data.name,
        description=data.description
    )


@router.delete(
    '/open_case',
    response_model=OpenCaseModel,
    summary='Удалить кейс'
)
async def delete_open_case(
        open_case_uuid: Union[str, UUID],
        db: CrudOpenCase = Depends(get_crud_open_case),
        current_user: UserModel = Depends(get_current_user)
):
    return await db.delete_open_case(
        open_case_uuid=open_case_uuid,
        profile_id=current_user.profile_id,
    )


@router.post(
    '/open_case/{open_case_uuid}/action',
    response_model=OpenCaseModel,
    summary='Запустить/Остановить открытие кейса'
)
async def launch_open_case(
        open_case_uuid: Union[str, UUID],
        is_active: bool,
        db: CrudOpenCase = Depends(get_crud_open_case),
        current_user: UserModel = Depends(get_current_user)
):
    if is_active:
        await db.stop_all_open_cases(current_user.profile_id)
    return await db.update_open_case(
        open_case_uuid=open_case_uuid,
        profile_id=current_user.profile_id,
        is_active=is_active
    )
