from datetime import datetime

import aiohttp
from fastapi_mail import MessageSchema, FastMail

from src.smtp_config import mail_conf


class MessageManager:

    @staticmethod
    async def send_email_registration(password: str,email: str):
        """
        Отправить email-уведомление о регистрации в системе HP Employers

        Args:
            email: Email адрес получателя (логин)
            password: Пароль для входа в систему
        """
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #2a52be;">Добро пожаловать в HP Employers!</h2>
            <p>Вы успешно зарегистрированы в системе.</p>

            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="margin-top: 0;">Ваши данные для входа:</h3>
                <p><strong>Логин (email):</strong> {email}</p>
                <p><strong>Пароль:</strong> {password}</p>
            </div>

            <p>Рекомендуем изменить пароль после первого входа в систему.</p>

            <p style="color: #666; font-size: 12px;">
                Это автоматическое сообщение, пожалуйста, не отвечайте на него.
                <br>Дата отправки: {datetime.now().strftime('%d.%m.%Y %H:%M')}
            </p>
        </body>
        </html>
        """

        message = MessageSchema(
            subject="✅ Регистрация в HP Employers",
            recipients=[email],
            body=html_content,
            subtype="html"
        )

        fm = FastMail(mail_conf)
        await fm.send_message(message)

    @staticmethod
    async def send_message_to_bot(text: str):
        url = "http://localhost:8080/send_message"
        payload = {"text": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    # logger.info("Сообщение успешно отправлено в Telegram.")
                    return True
                else:
                    # logger.error(f"Ошибка при отправке сообщения: {await response.text()}")
                    return False