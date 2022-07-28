from typing import List, Union, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.middleware.user import get_current_user
from api.v1.render_template.crud import CrudRenderTemplate, get_crud_render_template
from api.v1.render_template.schema import RenderTemplateBaseModel, RenderTemplateModel, RenderTemplateUpdateModel
from api.v1.user.schema import UserModel

router = APIRouter()


@router.post(
    "/render_template",
    status_code=201,
    response_model=RenderTemplateModel,
    summary="Добавить новый шаблон"
)
async def create_render_template(
        data: RenderTemplateBaseModel,
        db: CrudRenderTemplate = Depends(get_crud_render_template),
        current_user: UserModel = Depends(get_current_user)
):
    return await db.create_render_template(
        profile_id=current_user.profile_id,
        name=data.name,
        html_text=data.html_text,
        script_text=data.script_text,
        style_text=data.style_text,
        is_private=data.is_private
    )


@router.get(
    '/render_template',
    response_model=Union[List[RenderTemplateModel], RenderTemplateModel],
    summary='Получить шаблон'
)
async def get_render_template(
        render_template_uuid: Optional[Union[str, UUID]] = None,
        db: CrudRenderTemplate = Depends(get_crud_render_template),
        current_user: UserModel = Depends(get_current_user)
):
    if render_template_uuid:
        return await db.get_render_template_by_uuid(profile_id=current_user.profile_id,
                                                    render_template_uuid=render_template_uuid)
    return await db.get_render_templates(profile_id=current_user.profile_id)


@router.patch(
    '/render_template',
    response_model=RenderTemplateModel,
    summary='Обновить шаблон'
)
async def update_render_template(
        render_template_uuid: Union[str, UUID],
        data: RenderTemplateUpdateModel,
        db: CrudRenderTemplate = Depends(get_crud_render_template),
        current_user: UserModel = Depends(get_current_user)
):
    data_without_none = data.dict(exclude_none=True)
    if not data_without_none:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return await db.update_render_template(
        profile_id=current_user.profile_id,
        render_template_uuid=render_template_uuid,
        **data_without_none
    )


@router.delete(
    '/render_template',
    response_model=RenderTemplateModel,
    summary='Удалить шаблон'
)
async def delete_render_template(
        render_template_uuid: Union[str, UUID],
        db: CrudRenderTemplate = Depends(get_crud_render_template),
        current_user: UserModel = Depends(get_current_user)
):
    return await db.delete_render_template(
        render_template_uuid=render_template_uuid,
        profile_id=current_user.profile_id,
    )
