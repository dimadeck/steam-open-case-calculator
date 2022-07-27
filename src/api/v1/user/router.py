from starlette.requests import Request

from api.middleware.token import create_access_token
from api.v1.user.steamsignin import SteamSignIn

from fastapi import APIRouter, Depends

from api.v1.user.crud import UserCRUD, get_crud_user
from config import settings_app
from core.steam_info import SteamInfo

router = APIRouter()


@router.get(
    '/steam-login',
    summary='Авторизация steam'
)
async def login(steam_signin: SteamSignIn = Depends(SteamSignIn)):
    url = steam_signin.construct_url(settings_app.BACKEND_URL + '/process-login')
    return steam_signin.redirect_user(url)


@router.get(
    '/process-login',
    summary='Авторизация steam'
)
async def process_login(
        request: Request,
        steam_signin: SteamSignIn = Depends(SteamSignIn),
        user_crud: UserCRUD = Depends(get_crud_user)
):
    profile_id = steam_signin.validate_results(request.query_params)
    si = SteamInfo(int(profile_id))
    user_data = si.get_info()
    user = await user_crud.create_or_update(
        profile_id=user_data['profile_id'],
        username=user_data['username'],
        image_url=user_data['image_url']
    )
    return {
        "access_token": create_access_token(sub=user.profile_id),
        "token_type": "bearer",
        "profile_id": user.profile_id,
    }
