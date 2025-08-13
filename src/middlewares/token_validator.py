from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from src.utils.jwt_tokens import ALGORITHM, SECRET_KEY


class TokenValidationMiddleware(BaseHTTPMiddleware):
    excluded_paths = {'/auth/token', '/auth/refresh', '/auth/logout',
                      '/docs', '/favicon.ico', '/openapi.json','/auth/request-password-reset',
                      '/auth/verify-reset-token', '/auth/reset-password'
                      }

    async def dispatch(self, request: Request, call_next):
        # Пропускаем исключенные пути
        if request.url.path in self.excluded_paths:
            print('Пропускаем исключенные пути')
            return await call_next(request)

        try:
            # Получаем access_token из кук
            access_token = request.cookies.get("access_token")
            if not access_token:
                print('Access token missing')
                raise HTTPException(
                    status_code=401,
                    detail="Access token missing"
                )

            # Декодируем и валидируем токен
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token payload"
                )

            # Проверка IP (если нужно)
            if "ip" in payload:
                client_ip = request.client.host
                if payload["ip"] != client_ip:
                    raise HTTPException(
                        status_code=401,
                        detail="IP address changed"
                    )

            return await call_next(request)

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token expired"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        except (JWTError, HTTPException) as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e.detail) if hasattr(e, 'detail') else "Invalid token"},
                headers={"WWW-Authenticate": "Bearer"}
            )
