from typing import MutableMapping, List, Union
from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer

from config import settings_app

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]
oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='api/v1/steam-login', tokenUrl='api/v1/process-login')
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/v1/steam-login")


def create_access_token(*, sub: int) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings_app.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: int,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = sub

    return jwt.encode(payload, settings_app.JWT_SECRET, algorithm=settings_app.JWT_ALGORITHM)


def remove_token_type_in_token(token: str):
    if token.lower().startswith('bearer'):
        token = token.replace('Bearer ', '')
    return token


def decode_jwt(token: str = Depends(oauth2_scheme)):
    reformat_token = remove_token_type_in_token(token)

    try:
        payload = jwt.decode(
            reformat_token,
            settings_app.JWT_SECRET,
            algorithms=[settings_app.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        profile_id: str = payload.get("sub")
        return profile_id

    except Exception as e:
        print(e)
