from redis import Redis, ConnectionPool
import os
import logging

from src.config import REDIS_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


sync_redis_pool: ConnectionPool | None = None


def init_sync_redis() -> None:
    global sync_redis_pool
    try:
        sync_redis_pool = ConnectionPool.from_url(
            REDIS_URL,
            decode_responses=True,
            max_connections=100,
            socket_timeout=5,
            socket_connect_timeout=5
        )
        with Redis(connection_pool=sync_redis_pool) as redis:
            redis.ping()
        logger.info("Sync Redis pool connected")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise


def close_sync_redis() -> None:
    global sync_redis_pool
    if sync_redis_pool:
        sync_redis_pool.disconnect()
        logger.info("Sync Redis pool disconnected")


def get_sync_redis() -> Redis:
    global sync_redis_pool
    if sync_redis_pool is None:
        init_sync_redis()
    return Redis(connection_pool=sync_redis_pool)
