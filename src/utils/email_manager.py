import random
from datetime import datetime

import aiohttp
from fastapi import HTTPException
from fastapi_mail import MessageSchema, FastMail
from redis.asyncio import Redis

from src.config import VERIFICATION_CODE_TTL
from src.smtp_config import mail_conf


class EmailManager:
    def __init__(self,email:str):
        self.email = email

    async def send_code(self,redis:Redis):
        existing_code = await redis.get(f"email_verification:{self.email}")
        if existing_code:
            remaining_ttl = await redis.ttl(f"email_verification:{self.email}")
            raise HTTPException(
                status_code=400,
                detail=f"Код уже отправлен. Повторная отправка возможна через {remaining_ttl} секунд"
            )

        # Генерация 6-значного кода
        code = str(random.randint(100000, 999999))

        # Сохраняем код в Redis
        await redis.setex(
            f"email_verification:{self.email}",
            VERIFICATION_CODE_TTL,
            code
        )

        # Отправка email с кодом
        message = MessageSchema(
            subject="Код подтверждения email",
            recipients=[self.email],
            body=f"Ваш код подтверждения: {code}",
            subtype="plain"
        )

        fm = FastMail(mail_conf)
        await fm.send_message(message)

    async def verify_email_and_code(self,redis:Redis,code):
        stored_code = await redis.get(f"email_verification:{self.email}")

        if not stored_code:
            raise HTTPException(status_code=400, detail="Код не найден или истёк")

        if stored_code != code:
            # Уменьшаем количество попыток или блокируем после нескольких ошибок
            await self._handle_failed_attempt(redis)
            raise HTTPException(status_code=400, detail="Неверный код подтверждения")

        # Если код верный, удаляем его из Redis
        await redis.delete(f"email_verification:{self.email}")
        return True



    async def _handle_failed_attempt(self,redis: Redis):
        """Обработка неудачных попыток ввода кода"""
        attempt_key = f"email_attempts:{self.email}"
        attempts = await redis.incr(attempt_key)

        if attempts >= 3:
            # Блокируем на 5 минут после 3 неудачных попыток
            await redis.setex(attempt_key, 300, attempts)
            raise HTTPException(
                status_code=429,
                detail="Слишком много попыток. Попробуйте позже."
            )

        # Устанавливаем TTL для счётчика попыток
        await redis.expire(attempt_key, VERIFICATION_CODE_TTL)


