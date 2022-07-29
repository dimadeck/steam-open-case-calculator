import json
import os.path
from asyncio import sleep
from typing import List, Union, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket

from api.middleware.user import get_current_user
from api.v1.item.crud import get_crud_item, CrudItem
from api.v1.open_case.crud import CrudOpenCase, get_crud_open_case
from api.v1.open_case.schema import OpenCaseBaseModel, OpenCaseModel, OpenCaseUpdateModel, TaskModel
from api.v1.render_template.crud import CrudRenderTemplate, get_crud_render_template
from api.v1.user.schema import UserModel
from config import settings_app
from log import get_log_channel
from workers.redis_pub_sub import subscriber
from workers.tasks import launch_observer

templates = Jinja2Templates(directory=os.path.join('api', 'v1', 'templates'))

router = APIRouter()
_log = get_log_channel('Router')


@router.post(
    "/open_case",
    status_code=201,
    response_model=OpenCaseModel,
    summary="Добавить новое открытие кейсов"
)
async def create_open_case(
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
        return await db.get_open_case_by_uuid(profile_id=current_user.profile_id, open_case_uuid=open_case_uuid,
                                              with_items=with_items)
    return await db.get_open_cases(profile_id=current_user.profile_id, with_items=with_items)


@router.patch(
    '/open_case',
    response_model=OpenCaseModel,
    summary='Обновить кейс'
)
async def update_open_case(
        open_case_uuid: Union[str, UUID],
        data: OpenCaseUpdateModel,
        db: CrudOpenCase = Depends(get_crud_open_case),
        current_user: UserModel = Depends(get_current_user)
):
    data_without_none = data.dict(exclude_none=True)
    if not data_without_none:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return await db.update_open_case(
        profile_id=current_user.profile_id,
        open_case_uuid=open_case_uuid,
        **data_without_none
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
    response_model=Union[OpenCaseModel, TaskModel],
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
        open_case = await db.get_open_case_by_uuid(profile_id=current_user.profile_id, open_case_uuid=open_case_uuid)
        await db.update_open_case(
            open_case_uuid=open_case_uuid,
            profile_id=current_user.profile_id,
            is_active=is_active
        )
        task = launch_observer.delay(profile_id=open_case.profile_id, open_case_uuid=open_case.uuid)
        return {"task_id": task.id}
    return await db.update_open_case(
        open_case_uuid=open_case_uuid,
        profile_id=current_user.profile_id,
        is_active=is_active
    )


@router.get(
    '/open_case/{open_case_uuid}/render',
    summary='Страница рендера для открытия кейса'
)
async def render_open_case(
        request: Request,
        open_case_uuid: Union[str, UUID],
        db: CrudOpenCase = Depends(get_crud_open_case),
        render_template_crud: CrudRenderTemplate = Depends(get_crud_render_template),
):
    open_case = await db.get_open_case_by_uuid_without_user(open_case_uuid=open_case_uuid)
    # render_template = await render_template_crud.get_render_template_by_uuid(
    #     profile_id=open_case.profile_id,
    #     render_template_uuid=open_case.render_template_uuid
    # )
    data = {
        "request": request,
        "open_case": open_case,
        "data": {
            "backend_url": '127.0.0.1:8004/api/v1',
            "token": settings_app.BACKEND_TOKEN,
            "schema": "http://"
        }
    }
    return templates.TemplateResponse("render_page.html", data)


@router.websocket("/open_case/{open_case_uuid}/get_updates")
async def get_updates(
        websocket: WebSocket,
        open_case_uuid: Union[str, UUID],
        db: CrudItem = Depends(get_crud_item),
):
    await websocket.accept()

    while True:
        await sleep(1)
        try:
            message = subscriber.get_message()
            if message:
                _log.warning("MESSAGE: %s", message)
                item = json.loads(message['data'].decode('utf-8'))
                if item['open_case_uuid'] != open_case_uuid:
                    continue
                _log.warning(f'New Item: {item}')
                await websocket.send_text(json.dumps(item))
                _log.warning("MESSAGE: %s", message)

        except Exception as e:
            _log.error("WS ERROR: %s", str(e))
