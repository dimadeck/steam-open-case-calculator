from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class UserModel(BaseModelORM):
    profile_id: int
    username: str
    image_url: str
