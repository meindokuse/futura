from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Request, Response, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from passlib.context import CryptContext

SECRET_KEY = "SECRET_KEY"
REFRESH_SECRET_KEY = "REFRESH_SECRET_KEY"
ALGORITHM = "HS256"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str
    status: Optional[str] = None


class TokenData(BaseModel):
    id: str
    roles: list
    ip: Optional[str] = None


async def get_token_from_cookie(request: Request, access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return access_token


async def get_current_user(request: Request, token: Annotated[str, Depends(get_token_from_cookie)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        roles: list = payload.get("roles")

        if id is None or roles is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        if payload.get("ip"):
            client_ip = request.client.host
            if payload.get("ip") != client_ip:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="IP address changed"
                )

        return TokenData(id=id, roles=roles)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


user_dep = Annotated[TokenData, Depends(get_current_user)]


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def create_tokens(user_id: str, roles: list, ip: str):
    access_token = create_access_token(
        {"sub": user_id, "roles": roles},
        expires_delta=timedelta(minutes=15)
    )

    refresh_token = create_refresh_token(
        {"sub": user_id, "roles": roles, "ip": ip},
        expires_delta=timedelta(days=7)
    )

    return access_token, refresh_token


async def validate_refresh_token(refresh_token: str, ip: str) -> TokenData:
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        roles = payload.get("roles")
        token_ip = payload.get("ip")

        if user_id is None or roles is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if token_ip != ip:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token IP mismatch"
            )

        return TokenData(id=user_id, roles=roles, ip=ip)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


async def refresh_tokens(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is missing"
        )

    client_ip = request.client.host
    try:
        token_data = await validate_refresh_token(refresh_token, client_ip)

        new_access_token, new_refresh_token = create_tokens(
            user_id=token_data.id,
            roles=token_data.roles,
            ip=client_ip
        )

        # Обновляем ОБА токена в куках
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=int(timedelta(minutes=15).total_seconds())
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=int(timedelta(days=7).total_seconds())
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        print(f"Refresh error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Token refresh failed"
        )