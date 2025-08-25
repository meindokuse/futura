from typing import List, Dict

from src.celery.celery_app import app
import json
import logging
import asyncio
from datetime import date

from redis import ConnectionError

from src.data.unitofwork import UnitOfWork
from src.db.cache import get_sync_redis
from src.schemas.items import WorkDayRead, WorkDayFilter
from src.schemas.work_day import CustomJSONEncoder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3)
def update_schedule_cache_after_add(self, year: int, month: int, location_id: int):
    key = f"schedule:{year}-{month}:{location_id}"
    try:
        async def fetch_schedule():
            async with UnitOfWork() as uow:
                filters = WorkDayFilter(
                    employer_fio=None,
                    location_id=location_id,
                    work_type=None,
                )
                schedule = await uow.work_day.get_filtered(filters=filters, month_date=date(year, month, 1))
                return [s.model_dump() for s in schedule]

        schedule_data = asyncio.run(fetch_schedule())

        try:
            redis = get_sync_redis()
            serialized = json.dumps(schedule_data, cls=CustomJSONEncoder)
            redis.set(key, serialized, ex=120)
            logger.info(f"Cache updated for {key}")
        except ConnectionError as e:
            logger.error(f"Failed to set cache for {key}: {e}")
            raise self.retry(exc=e, countdown=60)

        return "Cache updated"
    except Exception as e:
        logger.error(f"Cache update error for {key}, attempt {self.request.retries + 1}: {e}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, max_retries=3)
def update_schedule_cache_with_data(self, year: int, month: int, location_id: int, schedule_data: List[WorkDayRead]):
    key = f"schedule:{year}-{month}:{location_id}"
    try:
        redis = get_sync_redis()
        # Сериализуем с кастомным энкодером
        serialized = json.dumps(schedule_data, cls=CustomJSONEncoder)
        redis.set(key, serialized, ex=120)
        logger.info(f"Cache updated for {key}")
        return "Cache updated"
    except Exception as e:
        logger.error(f"Cache update error for {key}, attempt {self.request.retries + 1}: {e}")
        raise self.retry(exc=e, countdown=60)
