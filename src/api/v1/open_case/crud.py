from typing import Union, List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload

from api.middleware.orm_error import orm_error_handler
from db.connections import async_session
from db.models import OpenCase


class CrudOpenCase:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @orm_error_handler
    async def create_open_case(
            self,
            profile_id: int,
            name: str,
            description: str
    ) -> OpenCase:
        open_case = OpenCase(
            profile_id=profile_id,
            name=name,
            description=description
        )
        self.db_session.add(open_case)
        await self.db_session.flush()
        return open_case

    @orm_error_handler
    async def get_open_case_by_uuid_without_user(
            self,
            open_case_uuid: Union[UUID, str],
            with_items: bool = True
    ) -> OpenCase:
        sql = select(OpenCase).filter_by(uuid=open_case_uuid)
        if with_items:
            sql = sql.options(selectinload(OpenCase.items))
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    @orm_error_handler
    async def get_open_case_by_uuid(
            self,
            profile_id: int,
            open_case_uuid: Union[UUID, str],
            with_items: bool = True
    ) -> OpenCase:
        sql = select(OpenCase).filter_by(profile_id=profile_id, uuid=open_case_uuid)
        if with_items:
            sql = sql.options(selectinload(OpenCase.items))
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    @orm_error_handler
    async def get_open_cases(self, profile_id: int, with_items: bool = False) -> List[OpenCase]:
        sql = select(OpenCase).filter_by(profile_id=profile_id)
        if with_items:
            sql = sql.options(selectinload(OpenCase.items))
        query = await self.db_session.execute(sql)
        return query.scalars().all()

    @orm_error_handler
    async def update_open_case(self, profile_id: int, open_case_uuid: Union[UUID, str], **kwargs):
        sql = update(OpenCase).filter_by(profile_id=profile_id, uuid=open_case_uuid).values(**kwargs). \
            execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)
        return await self.get_open_case_by_uuid(profile_id=profile_id, open_case_uuid=open_case_uuid)

    @orm_error_handler
    async def stop_all_open_cases(self, profile_id: int):
        sql = update(OpenCase).filter_by(profile_id=profile_id).values(is_active=False). \
            execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)

    @orm_error_handler
    async def delete_open_case(self, profile_id: int, open_case_uuid: Union[UUID, str]):
        open_case = await self.get_open_case_by_uuid(profile_id=profile_id, open_case_uuid=open_case_uuid)
        await self.db_session.delete(open_case)


async def get_crud_open_case():
    async with async_session() as session:
        async with session.begin():
            yield CrudOpenCase(session)
