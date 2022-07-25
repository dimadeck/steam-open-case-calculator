from fastapi import FastAPI
from starlette.requests import Request
from api.v1.steam_auth.steamsignin import SteamSignIn

from fastapi import APIRouter, Depends

from config import settings_app
from core.steam_info import SteamInfo

router = APIRouter()

@router.get(
    '/steam-login',
    summary='Авторизация steam'
)
async def login(steam_signin: SteamSignIn = Depends(SteamSignIn)):
    url = steam_signin.ConstructURL(settings_app.BACKEND_URL + '/process-login')
    return steam_signin.RedirectUser(url)


@router.get(
    '/process-login',
    summary='Авторизация steam'
)
async def process_login(request: Request, steam_signin: SteamSignIn = Depends(SteamSignIn)):
    profile_id = steam_signin.ValidateResults(request.query_params)
    si = SteamInfo(profile_id)
    return si.get_info()
