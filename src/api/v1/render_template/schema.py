from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class RenderTemplateBaseModel(BaseModelORM):
    name: str
    html_text: str
    script_text: Optional[str] = ""
    style_text: Optional[str] = ""
    is_private: bool


class RenderTemplateUpdateModel(BaseModelORM):
    name: Optional[str]
    html_text: Optional[str]
    script_text: Optional[str]
    style_text: Optional[str]
    is_private: Optional[bool]


class RenderTemplateModel(RenderTemplateBaseModel):
    uuid: Union[str, UUID]
    profile_id: str
