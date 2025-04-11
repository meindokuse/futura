import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import HTTPException
from redis.asyncio import Redis
from fastapi import BackgroundTasks
from src.data.unitofwork import IUnitOfWork
from src.schemas.items import WorkDayRead, WorkDayFilter

from src.schemas.work_day import WorkDayCreate
from datetime import date

class WorkService:
    async def _update_cache(self, cache_key: str, data: List[WorkDayRead], redis_client: Redis):
        # Преобразуем каждый объект WorkDayRead в словарь и обрабатываем datetime
        dict_data = [x.model_dump_ext() for x in data]
        await redis_client.setex(cache_key, 300, json.dumps(dict_data))  # Сериализуем в JSON

    async def get_schedule(self, uow: IUnitOfWork, page: int, limit: int, location_id: id, redis_client: Redis,
                           background_tasks: BackgroundTasks):
        cache_key = f"schedule:page_{page}:location_id_{location_id}"
        cached_schedule = await redis_client.get(cache_key)
        if cached_schedule:
            return json.loads(cached_schedule)
        async with uow:
            schedule_data = await uow.work_day.get_workdays(page=page, limit=limit, location_id=location_id)
            background_tasks.add_task(self._update_cache, cache_key, schedule_data, redis_client)
            return schedule_data

    async def get_schedule_filter(self, uow: IUnitOfWork, filters: WorkDayFilter, date_filter:Optional[date] = None):
        async with uow:
            schedule = await uow.work_day.get_filtered(filters=filters,date_filter=date_filter)
            return schedule


    async def get_list_workdays(self, uow: IUnitOfWork, page: int, limit: int, location_id: int):
        async with uow:
            res = await uow.work_day.get_workdays(page=page, limit=limit, location_id=location_id)
            return res

    async def get_list_workdays_for_current_employer(self, uow: IUnitOfWork, fio: str, page: int, limit: int,
                                                     location_id: int):
        async with uow:
            res = await uow.work_day.get_workdays_by_fio(fio=fio, page=page, limit=limit, location_id=location_id)
            return res

    async def get_list_workdays_for_current_day(self, uow: IUnitOfWork, work_day: datetime.date, page: int, limit: int,
                                                location_id: int):
        async with uow:
            res = await uow.work_day.get_workdays_by_date(work_day, page, limit, location_id=location_id)
            return res

    async def add_employers_to_work(self, uow: IUnitOfWork, workday: WorkDayCreate):
        if workday.work_time.tzinfo is not None:
            workday.work_time = workday.work_time.replace(tzinfo=None)
            raise HTTPException(status_code=500)
        data = workday.model_dump()
        async with uow:
            await uow.work_day.add_one(data=data)
            await uow.commit()

    async def add_list_workdays(self, uow: IUnitOfWork, workdays: List[WorkDayCreate]):
        data = [x.model_dump() for x in workdays]
        async with uow:
            await uow.work_day.add_all(data_list=data)
            await uow.commit()

    async def delete_work_day(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.work_day.delete_one(id=id)
            await uow.commit()
