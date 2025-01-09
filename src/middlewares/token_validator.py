
from src.utils.jwt_tokens import SECRET_KEY, ALGORITHM

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from jose import jwt, JWTError


class TokenValidationMiddleware(BaseHTTPMiddleware):
    excluded_paths = {'/auth/login', '/auth/logout'}

    async def dispatch(self, request: Request, call_next):
        # Пропуск путей, которые не требуют проверки
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return RedirectResponse(url="/auth/login", status_code=307)

        token = token[7:]  # Убираем "Bearer " из начала токена

        try:
            # Валидация токена
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            fio: str = payload.get("sub")

            if fio is None:
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate user."
                )

        except JWTError:
            return RedirectResponse(url="/auth/login", status_code=307)

        return await call_next(request)
