from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class ItemModelBase(BaseModelORM):
    open_case_uuid: Union[str, UUID]
    asset_id: int
    class_id: int
    instance_id: Optional[int] = 0
    name: Optional[str] = None
    item_type: Optional[str] = None
    weapon: Optional[str] = None
    exterior: Optional[str] = None
    rarity: Optional[str] = None
    rarity_color: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    item_float: Optional[float] = 0.0


class ItemModel(ItemModelBase):
    profile_id: int
    is_shown: bool
