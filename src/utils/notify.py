import asyncio

import aiohttp


async def send_message_to_bot(text: str):
    url = "http://localhost:8080/send_message"
    payload = {"text": text}
    await asyncio.sleep(3)


    async with aiohttp.ClientSession() as session:
        # try:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                # logger.info("Сообщение успешно отправлено в Telegram.")
                return True
            else:
                # logger.error(f"Ошибка при отправке сообщения: {await response.text()}")
                return False
