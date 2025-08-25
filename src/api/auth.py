import random
import secrets
from datetime import timedelta, datetime
from typing import Annotated

import jwt
import redis
from fastapi import APIRouter, Response, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema
from redis.asyncio import Redis
from starlette.responses import JSONResponse

from src.api.dependses import UOWDep
from src.config import VERIFICATION_CODE_TTL
from src.db.async_cache import get_redis
from src.models.items import LogType, LogAction
from src.schemas.logs import LogsCreate
from src.schemas.other_requests import EmailRequest, VerifyEmailRequest, PasswordRequest, ResetPasswordRequest, \
    NewPasswordRequest
from src.schemas.peoples import EmployerCreate
from src.services.employer_service import EmployerService
from src.services.work_service import WorkService
from src.smtp_config import mail_conf
from src.utils.jwt_tokens import create_access_token, user_dep, Token, create_tokens, REFRESH_TOKEN_COOKIE_NAME, \
    refresh_tokens, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

from src.utils.email_manager import EmailManager
from src.utils.password_manager import PasswordManager

router = APIRouter(
    tags=['auth'],
    prefix='/auth',
)


@router.post('/token')
async def login_for_get_token(
        response: Response,
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        uow: UOWDep
):
    # try:
    # Аутентификация пользователя
    user = await EmployerService().authenticate(uow, form_data.username, form_data.password)
    if not user:
        return {'status': False}

    client_ip = request.client.host
    access_token, refresh_token = create_tokens(
        user_id=str(user.id),
        is_admin=user.is_admin,
        ip=client_ip
    )

    # Устанавливаем ОБА токена в HTTP-only куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=15).total_seconds())  # TTL access token
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(days=7).total_seconds())  # TTL refresh token
    )

    return {
        "access_token": access_token,  # Теперь возвращаем токен и в теле ответа
        "token_type": "bearer",
        "status": True
    }


@router.post('/refresh', response_model=Token)
async def refresh_token_pair(
        request: Request,
        response: Response
):
    return await refresh_tokens(request, response)


@router.get('/profile')
async def get_profile(user: user_dep, uow: UOWDep):
    user_data = await EmployerService().get_current_employer(uow, int(user.id))
    return {
        "user": user_data,
    }


@router.get('/check_admin')
async def check_admin(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication required"},
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    is_admin = payload.get("is_admin")

    # Проверяем наличие хотя бы одной роли, начинающейся с "admin"
    if not is_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin access denied"
        )
    return JSONResponse(
        status_code=200,
        content={"detail": "Admin access required"},
    )


@router.post("/send-verification-code")
async def send_verification_code(
        request: EmailRequest,  # Принимаем JSON
        uow: UOWDep,
        redis: Redis = Depends(get_redis)
):
    email = request.email  # Получаем email из JSON тела

    employer_service = EmployerService()
    is_exist = await employer_service.is_exist_email(uow, email)

    if is_exist:
        raise HTTPException(status_code=409, detail='Email already registered')

    email_manager = EmailManager(email)
    await email_manager.send_code(redis)
    return {"message": "Код подтверждения отправлен"}


@router.post("/verify-email")
async def verify_email(
        request: VerifyEmailRequest,  # Принимаем данные как JSON тело
        user: user_dep,
        uow: UOWDep,
        redis: Redis = Depends(get_redis)
):
    # Получаем код из Redis
    email_manager = EmailManager(request.email)
    is_success = await email_manager.verify_email_and_code(redis, request.code)

    if not is_success:
        raise HTTPException(
            status_code=400,
            detail="Неверный код подтверждения"
        )

    employer_service = EmployerService()
    await employer_service.edit_email(uow, request.email, int(user.id))

    return {"message": "Email успешно изменен"}


@router.post('/change-password')
async def change_password(
        request: PasswordRequest,
        user: user_dep,
        uow: UOWDep,
):
    employer_service = EmployerService()
    success = await employer_service.edit_password(
        uow,
        request.current_password,
        request.new_password,
        int(user.id)
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Неверный текущий пароль"
        )

    return {"status": "success", "message": "Пароль успешно изменен"}


@router.post('/admin/register')
async def register(new_user: EmployerCreate, uow: UOWDep, user: user_dep):
    id = await EmployerService().add_employer(uow, new_user, int(user.id))
    return {
        'status': 'success',
        'id': id
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {"message": "Logged out successfully"}


@router.post("/request-password-reset")
async def request_reset_link(
        uow: UOWDep,
        request: Request,
        data: ResetPasswordRequest,
        redis: Redis = Depends(get_redis),
):
    is_valid = await EmployerService().validate_email(data.email, uow)
    if not is_valid:
        raise HTTPException(status_code=404, detail="Email is not registered")

    password_manager = PasswordManager(redis)
    await password_manager.save_code_and_send(request, data.email)
    return {'status': 'success'}


@router.get("/verify-reset-token")
async def verify_reset_token(token: str, redis: Redis = Depends(get_redis)):
    password_manager = PasswordManager(redis)
    return await password_manager.verify_reset_token(token)


@router.post("/reset-password")
async def reset_password(
        uow: UOWDep,
        data: NewPasswordRequest,
        redis: Redis = Depends(get_redis),
):
    password_manager = PasswordManager(redis)
    email = await password_manager.clear_redis(data.token)

    employer_service = EmployerService()
    await employer_service.edit_password_after_validate(uow, data.new_password, email)
