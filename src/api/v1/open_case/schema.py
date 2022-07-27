import datetime
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel, validator, Field

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
    total_amount: Optional[int]
    total_count: Optional[int]

    @validator('total_amount', always=True, check_fields=False)
    def get_total_amount(cls, _, values):
        total_amount = 0
        for item in values.get('items', []):
            total_amount += item.price
        return total_amount

    @validator('total_count', always=True, check_fields=False)
    def get_total_count(cls, _, values):
        return len(values.get('items', []))


# class OpenCaseModelWithoutItems(OpenCaseModel):
#     items: List[ItemModel] = Field(exclude=True)
