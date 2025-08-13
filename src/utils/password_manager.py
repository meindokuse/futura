import secrets

from fastapi_mail import MessageSchema, FastMail
from redis.asyncio import Redis
from fastapi import Request, HTTPException

from src.config import VERIFICATION_CODE_TTL
from src.smtp_config import mail_conf


class PasswordManager:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_code_and_send(self, request: Request, email: str):
        # Генерация 6-значного кода
        token = secrets.token_urlsafe(32)
        # Сохраняем код в Redis
        await self.redis.setex(
            f"password_reset:{token}",
            3600,
            email,
        )
        reset_link = f"{request.base_url}reset-password?token={token}"

        # Отправка email с кодом
        message = MessageSchema(
            subject="Ссылка сброса для пароля",
            recipients=[email],
            body=f"Ваша ссылка для сброса пароля: {reset_link}",
            subtype="plain"
        )

        fm = FastMail(mail_conf)
        await fm.send_message(message)

    async def verify_reset_token(self, token: str):
        email = await self.redis.get(f"password_reset:{token}")
        if not email:
            raise HTTPException(status_code=400, detail="Недействительная или устаревшая ссылка")

        return email

    async def clear_redis(self,token: str):
        email = await self.redis.get(f"password_reset:{token}")

        if not email:
            raise HTTPException(status_code=400, detail="Недействительная или устаревшая ссылка")

        await self.redis.delete(f"password_reset:{token}")
        return email
