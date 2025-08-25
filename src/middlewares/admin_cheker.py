import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from src.utils.jwt_tokens import SECRET_KEY, ALGORITHM, get_token_from_cookie

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
        token = await get_token_from_cookie(request)

        if not token:
            print('тут')
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        try:
            # Декодируем токен
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            is_admin = payload.get("is_admin")

            if not is_admin:
                raise HTTPException(
                    status_code=403,
                    detail="Admin access required"
                )


        except JWTError:
            print('или тут')
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
