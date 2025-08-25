import httpx

from src.celery.celery_app import app
from src.config import BOT_URL


@app.task(bind=True, max_retries=3)
def bot_send_task(self, text: str):
    url = f"{BOT_URL}send_message"
    payload = {"text": text}

    try:
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=10.0)

            if response.status_code == 200:
                # logger.info("Сообщение успешно отправлено в Telegram.")
                return True
            else:
                # logger.error(f"Ошибка при отправке сообщения: {response.text}")
                self.retry(countdown=60)  # Повтор через 60 секунд
                return False

    except httpx.RequestError as e:
        # logger.error(f"Сетевая ошибка: {e}")
        self.retry(countdown=60)
        return False
