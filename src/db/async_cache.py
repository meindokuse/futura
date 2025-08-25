from redis.asyncio import Redis, ConnectionPool, ConnectionError
import os
import logging
from typing import AsyncGenerator

from src.config import REDIS_URL

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальный пул соединений
redis_pool: ConnectionPool | None = None


async def init_redis() -> None:
    global redis_pool
    try:
        redis_pool = ConnectionPool.from_url(
            REDIS_URL,
            decode_responses=True,
            max_connections=100,
            socket_timeout=5,
            socket_connect_timeout=5
        )
        # Проверяем подключение
        async with Redis(connection_pool=redis_pool) as redis:
            await redis.ping()
        logger.info("Redis pool connected successfully")
    except ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise


async def close_redis() -> None:
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()
        logger.info("Redis pool disconnected")


async def get_redis() -> AsyncGenerator[Redis, None]:
    global redis_pool
    if redis_pool is None:
        raise RuntimeError("Redis pool not initialized")
    async with Redis(connection_pool=redis_pool) as redis:
        yield redis
