from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Request, Response, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from passlib.context import CryptContext
from src.config import SECRET_KEY, REFRESH_SECRET_KEY

ALGORITHM = "HS256"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str
    status: Optional[bool] = None


class TokenData(BaseModel):
    id: str
    is_admin: bool
    ip: Optional[str] = None


async def get_token_from_cookie(request: Request):
    # Сначала проверяем request.state
    if hasattr(request.state, "access_token"):
        print(f"Token from request.state: {request.state.access_token}")
        return request.state.access_token

    # Иначе парсим cookies
    cookies = {}
    cookie_header = request.headers.get("cookie", "")
    if cookie_header:
        try:
            for cookie in cookie_header.split("; "):
                if "=" in cookie:
                    key, value = cookie.split("=", 1)
                    cookies[key] = value
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid cookie format")

    token = cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token missing")
    print(f"Token from cookies: {token}")
    return token


async def get_current_user(request: Request, token: str = Depends(get_token_from_cookie)):
    try:
        print('get_current_user', token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin")

        if id is None or is_admin is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return TokenData(id=id, is_admin=is_admin)

    except jwt.ExpiredSignatureError:
        print('в получении пользователя-ExpiredSignatureError')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        print('в получении пользователя-InvalidTokenError')
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


def create_tokens(user_id: str, is_admin: bool, ip: str):
    access_token = create_access_token(
        {"sub": user_id, "is_admin": is_admin},
        expires_delta=timedelta(minutes=1)
    )

    refresh_token = create_refresh_token(
        {"sub": user_id, "is_admin": is_admin, "ip": ip},
        expires_delta=timedelta(days=7)
    )

    return access_token, refresh_token


async def validate_refresh_token(refresh_token: str, ip: str) -> TokenData:
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        is_admin = payload.get("is_admin")
        token_ip = payload.get("ip")

        if user_id is None or is_admin is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if token_ip != ip:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token IP mismatch"
            )

        return TokenData(id=user_id, is_admin=is_admin, ip=ip)
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
            is_admin=token_data.is_admin,
            ip=client_ip
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    except Exception as e:
        print(f"Refresh error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Token refresh failed"
        )
