from sqlalchemy import select
from sqlalchemy.orm import Session

from db.connections import async_session
from db.models import User


class UserCRUD:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, profile_id: int, username: str, image_url: str) -> User:
        user = User(profile_id=profile_id, username=username, image_url=image_url)
        self.db_session.add(user)
        await self.db_session.flush()
        return user

    async def get_user(self, profile_id) -> User:
        sql = select(User).filter_by(profile_id=profile_id)
        query = await self.db_session.execute(sql)
        return query.scalar_one()


async def get_crud_user():
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)
