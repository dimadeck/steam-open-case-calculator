from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from api.middleware.orm_error import orm_error_handler
from db.connections import async_session
from db.models import User


class UserCRUD:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @orm_error_handler
    async def create(self, profile_id: int, username: str, image_url: str) -> User:
        user = User(profile_id=profile_id, username=username, image_url=image_url)
        self.db_session.add(user)
        await self.db_session.flush()
        return user

    @orm_error_handler
    async def get_user(self, profile_id: int) -> User:
        sql = select(User).filter_by(profile_id=profile_id)
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    @orm_error_handler
    async def update_user(self, profile_id: int, **kwargs):
        sql = update(User).filter_by(profile_id=profile_id).values(**kwargs). \
            execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)
        return await self.get_user(profile_id=profile_id)

    @orm_error_handler
    async def create_or_update(self, profile_id: int, username: str, image_url: str) -> User:
        try:
            user = await self.get_user(profile_id=profile_id)
            if user.username != username or user.image_url != image_url:
                user = await self.update_user(username=username, image_url=image_url)
            return user
        except NoResultFound as exc:
            return await self.create(profile_id=profile_id, username=username, image_url=image_url)


async def get_crud_user():
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)
