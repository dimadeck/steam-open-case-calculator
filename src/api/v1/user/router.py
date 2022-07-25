from fastapi import APIRouter, Depends

from api.v1.user.crud import UserCRUD, get_crud_user
from api.v1.user.schema import UserModel

router = APIRouter()

