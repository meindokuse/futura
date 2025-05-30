import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from src.utils.jwt_tokens import SECRET_KEY, ALGORITHM

from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError


class AdminRoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Проверяем, начинается ли путь с /admin
        if '/admin' not in request.url.path:
            print('нету админ пути')
            return await call_next(request)

        # Получаем токен из кук (или заголовков)
        token = request.cookies.get("access_token") or \
                (request.headers.get("Authorization") and request.headers["Authorization"][7:])

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        try:
            # Декодируем токен
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            roles = payload.get("roles", [])

            # Проверяем наличие хотя бы одной роли, начинающейся с "admin"
            if not any(role.startswith('admin') for role in roles):
                raise HTTPException(
                    status_code=403,
                    detail="Admin access required"
                )

            # Добавляем данные пользователя в request.state для использования в роутах
            request.state.user_id = payload.get("sub")
            request.state.roles = roles

        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        except HTTPException as he:
            return JSONResponse(
                status_code=he.status_code,
                content={"detail": he.detail}
            )

        except Exception:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

        return await call_next(request)
