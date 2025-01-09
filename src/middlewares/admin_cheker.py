import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from src.utils.jwt_tokens import SECRET_KEY, ALGORITHM


class AdminRoleMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token:
            # Редирект на логин, если токен отсутствует
            return RedirectResponse(url="/auth/login", status_code=307)

        try:
            token = token[7:]  # Убираем "Bearer " из начала токена

            # Декодируем токен
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            roles: str = payload.get("roles")
            if "admin" not in roles:  # Проверяем роль
                raise HTTPException(status_code=403, detail="Not enough permissions")
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=307)

        return await call_next(request)
