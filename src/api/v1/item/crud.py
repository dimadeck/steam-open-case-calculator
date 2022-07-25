from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from db.connections import async_session
from db.models import Item


class CrudItem:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_item(
            self,
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

    # async def get_item_by_name(self, name: str) -> Item:
    #     sql = select(Item).filter_by(name=name)
    #     query = await self.db_session.execute(sql)
    #     return query.scalar_one()
    # 
    # async def _get_item(self, item_id: int) -> Item:
    #     sql = select(Item).filter_by(id=item_id)
    #     query = await self.db_session.execute(sql)
    #     return query.scalar_one()
    # 
    # async def get_item_by_id(self, item_id: int) -> Item:
    #     return await self._get_item(item_id)
    # 
    async def get_items(self) -> List[Item]:
        sql = select(Item)
        query = await self.db_session.execute(sql)
        return query.scalars().all()

    async def show_items(self, profile_id: int) -> List[Item]:
        sql = select(Item).filter_by(profile_id=profile_id, is_shown=False)
        query = await self.db_session.execute(sql)
        items = query.scalars().all()
        for item in items:
            await self.update_item(item.asset_id, is_shown=True)
        return items

    async def update_item(self, asset_id: int, **kwargs):
        sql = update(Item).filter_by(asset_id=asset_id).values(**kwargs).execution_options(synchronize_session="fetch")
        await self.db_session.execute(sql)
    #
    # async def delete_item(self, item_id: int):
    #     item = await self._get_item(item_id)
    #     await self.db_session.delete(item)


async def get_crud_item():
    async with async_session() as session:
        async with session.begin():
            yield CrudItem(session)
