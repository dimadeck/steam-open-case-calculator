from fastapi import Depends

from api.middleware.token import decode_jwt, oauth2_scheme
from api.v1.user.crud import UserCRUD, get_crud_user


async def _get_user(token, crud_users):
    jwt_user_uuid = decode_jwt(token=token)
    user = await crud_users.get_user(jwt_user_uuid)
    return user


async def get_current_user(
        db: UserCRUD = Depends(get_crud_user),
        token: str = Depends(oauth2_scheme)
):
    return await _get_user(token, db)
