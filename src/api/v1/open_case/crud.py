from typing import Union, List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from db.connections import async_session
from db.models import OpenCase


class CrudOpenCase:
    def __init__(self, db_session: Session):
        self.db_session = db_session

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

    async def get_open_case_by_uuid(self, profile_id: int, open_case_uuid: Union[UUID, str]) -> OpenCase:
        sql = select(OpenCase).filter_by(profile_id=profile_id, uuid=open_case_uuid)
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    async def _get_open_case(self, profile_id: int, open_case_uuid: Union[UUID, str]) -> OpenCase:
        sql = select(OpenCase).filter_by(profile_id=profile_id, uuid=open_case_uuid)
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    async def get_open_cases(self, profile_id: int) -> List[OpenCase]:
        sql = select(OpenCase).filter_by(profile_id=profile_id)
        query = await self.db_session.execute(sql)
        return query.scalars().all()

    async def update_open_case(self, profile_id: int, open_case_uuid: Union[UUID, str], **kwargs):
        sql = update(OpenCase).filter_by(profile_id=profile_id, uuid=open_case_uuid).values(**kwargs).\
            execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)
        return await self._get_open_case(profile_id=profile_id, open_case_uuid=open_case_uuid)

    async def delete_open_case(self, profile_id: int, open_case_uuid: Union[UUID, str]):
        open_case = await self._get_open_case(profile_id=profile_id, open_case_uuid=open_case_uuid)
        await self.db_session.delete(open_case)


async def get_crud_open_case():
    async with async_session() as session:
        async with session.begin():
            yield CrudOpenCase(session)