from typing import Union, List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload

from api.middleware.orm_error import orm_error_handler
from db.connections import async_session
from db.models import RenderTemplate


class CrudRenderTemplate:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @orm_error_handler
    async def create_render_template(
            self,
            profile_id: int,
            name: str,
            html_text: str,
            script_text: Optional[str] = "",
            style_text: Optional[str] = "",
            is_private: Optional[bool] = False
    ) -> RenderTemplate:
        render_template = RenderTemplate(
            profile_id=profile_id,
            name=name,
            html_text=html_text,
            script_text=script_text,
            style_text=style_text,
            is_private=is_private,
        )
        self.db_session.add(render_template)
        await self.db_session.flush()
        return render_template

    @orm_error_handler
    async def get_render_template_by_uuid(
            self,
            profile_id: int,
            render_template_uuid: Union[UUID, str]
    ) -> RenderTemplate:
        sql = select(RenderTemplate).filter_by(profile_id=profile_id, uuid=render_template_uuid)
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    @orm_error_handler
    async def get_render_templates(self, profile_id: int) -> List[RenderTemplate]:
        sql = select(RenderTemplate).filter_by(profile_id=profile_id)
        query = await self.db_session.execute(sql)
        return query.scalars().all()

    @orm_error_handler
    async def update_render_template(self, profile_id: int, render_template_uuid: Union[UUID, str], **kwargs):
        sql = update(RenderTemplate).filter_by(profile_id=profile_id, uuid=render_template_uuid).values(**kwargs). \
            execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)
        return await self.get_render_template_by_uuid(profile_id=profile_id, render_template_uuid=render_template_uuid)

    @orm_error_handler
    async def delete_render_template(self, profile_id: int, render_template_uuid: Union[UUID, str]):
        render_template = await self.get_render_template_by_uuid(profile_id=profile_id,
                                                                 render_template_uuid=render_template_uuid)
        await self.db_session.delete(render_template)


async def get_crud_render_template():
    async with async_session() as session:
        async with session.begin():
            yield CrudRenderTemplate(session)
