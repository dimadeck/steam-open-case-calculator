from typing import Optional, List, Union
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from api.middleware.orm_error import orm_error_handler
from db.connections import async_session
from db.models import Item


class CrudItem:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @orm_error_handler
    async def create_item(
            self,
            open_case_uuid: Union[str, UUID],
            profile_id: int,
            asset_id: int,
            class_id: int,
            name: str,
            item_type: str,
            rarity_color: str,
            image_url: str,
            price: float,
            instance_id: Optional[int] = None,
            weapon: Optional[str] = None,
            exterior: Optional[str] = None,
            rarity: Optional[str] = None,
            item_float: Optional[float] = None
    ) -> Item:
        item = Item(
            open_case_uuid=open_case_uuid,
            profile_id=profile_id,
            asset_id=asset_id,
            class_id=class_id,
            instance_id=instance_id,
            name=name,
            item_type=item_type,
            weapon=weapon,
            exterior=exterior,
            rarity=rarity,
            rarity_color=rarity_color,
            image_url=image_url,
            price=price,
            item_float=item_float
        )
        self.db_session.add(item)
        await self.db_session.flush()
        return item

    @orm_error_handler
    async def get_items(
            self,
            profile_id: int,
            open_case_uuid: Optional[Union[str, UUID]] = None,
            is_shown=None
    ) -> List[Item]:
        kwargs = dict(profile_id=profile_id)
        if open_case_uuid:
            kwargs.update(dict(open_case_uuid=open_case_uuid))
        if is_shown is not None:
            kwargs.update(dict(is_shown=is_shown))
        sql = select(Item).filter_by(**kwargs)
        query = await self.db_session.execute(sql)
        return query.scalars().all()

    @orm_error_handler
    async def update_item(self, profile_id: int, asset_id: int, **kwargs):
        sql = update(Item).filter_by(profile_id=profile_id, asset_id=asset_id).values(**kwargs). \
            execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)


async def get_crud_item():
    async with async_session() as session:
        async with session.begin():
            yield CrudItem(session)
