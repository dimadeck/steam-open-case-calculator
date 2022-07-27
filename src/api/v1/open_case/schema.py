import datetime
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel

from api.v1.item.schema import ItemModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class OpenCaseBaseModel(BaseModelORM):
    name: str
    description: Optional[str] = None


class OpenCaseModel(OpenCaseBaseModel):
    uuid: Union[str, UUID]
    profile_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_active: bool
    items: List[ItemModel]
