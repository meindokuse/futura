from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from src.utils.jwt_tokens import ALGORITHM, refresh_tokens
from src.config import SECRET_KEY
from datetime import datetime

class TokenValidationMiddleware(BaseHTTPMiddleware):
    excluded_paths = {
        '/auth/token', '/auth/logout', '/docs', '/favicon.ico', '/openapi.json',
        '/auth/request-password-reset', '/auth/verify-reset-token', '/auth/reset-password'
    }

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        cookies = {}
        cookie_header = request.headers.get("cookie", "")
        if cookie_header:
            try:
                for cookie in cookie_header.split("; "):
                    if "=" in cookie:
                        key, value = cookie.split("=", 1)
                        cookies[key] = value
            except ValueError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid cookie format"},
                    headers={"WWW-Authenticate": "Bearer"}
                )

        access_token = cookies.get("access_token")
        refresh_token = cookies.get("refresh_token")
        print(f"Access token from cookies: {access_token}")

        if not access_token:
            return await self._handle_missing_access_token(request, refresh_token, call_next)

        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return await self._validate_payload_and_continue(request, payload, call_next)

        except jwt.ExpiredSignatureError:
            print('Access token expired, attempting to refresh', access_token)
            return await self._handle_token_refresh(request, refresh_token, call_next)

        except (JWTError, HTTPException) as e:
            print(f'Token validation error: {e}')
            return self._create_error_response(e)

    async def _handle_missing_access_token(self, request, refresh_token, call_next):
        print('Access token missing')
        if refresh_token:
            return await self._handle_token_refresh(request, refresh_token, call_next)
        else:
            print('No refresh_token found, returning 401')
            return JSONResponse(
                status_code=401,
                content={"detail": "Access token missing and no refresh_token"},
                headers={"WWW-Authenticate": "Bearer"}
            )

    async def _handle_token_refresh(self, request, refresh_token, call_next):
        try:
            response = Response()
            tokens = await refresh_tokens(request, response)

            # Устанавливаем куки в ответ для клиента
            response.set_cookie(
                key="access_token",
                value=tokens["access_token"],
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=900  # 15 минут
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh_token"],
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=604800  # 7 дней
            )

            # Сохраняем новый токен в request.state
            request.state.access_token = tokens["access_token"]
            request.state.refresh_token = tokens["refresh_token"]

            # Обновляем заголовки в request.scope
            new_cookie = f"access_token={tokens['access_token']}; refresh_token={tokens['refresh_token']}"
            new_headers = [(k.encode(), v.encode()) for k, v in request.headers.items() if k.lower() != "cookie"]
            new_headers.append(("cookie".encode(), new_cookie.encode()))
            request.scope["headers"] = new_headers

            print('новый токен', tokens["access_token"])
            print('токен в запросе', request.cookies.get("access_token"))

            # Вызываем следующий обработчик
            result = await call_next(request)
            if isinstance(result, Response):
                # Добавляем Set-Cookie заголовки из response
                for key, value in response.headers.items():
                    if key.lower() == "set-cookie":
                        result.headers.append("set-cookie", value)
            return result

        except HTTPException as e:
            print(f'Refresh error: {e.detail}')
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
                headers={"WWW-Authenticate": "Bearer"}
            )
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response

    async def _validate_payload_and_continue(self, request, payload, call_next):
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if "ip" in payload and payload["ip"] != request.client.host:
            raise HTTPException(status_code=401, detail="IP address changed")

        return await call_next(request)

    def _create_error_response(self, error):
        return JSONResponse(
            status_code=401,
            content={"detail": str(error.detail) if hasattr(error, 'detail') else "Invalid token"},
            headers={"WWW-Authenticate": "Bearer"}
        )