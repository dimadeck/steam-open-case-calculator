import datetime
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel, validator, Field

from api.v1.item.schema import ItemModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class RenderTemplateBaseModel(BaseModelORM):
    name: str
    html_text: str
    script_text: Optional[str] = ""
    style_text: Optional[str] = ""
    is_private: bool


class RenderTemplateModel(RenderTemplateBaseModel):
    uuid: str
    profile_id: str
