import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import HTTPException
from redis.asyncio import Redis
from fastapi import BackgroundTasks
from src.data.unitofwork import IUnitOfWork
from src.schemas.items import WorkDayRead, WorkDayFilter

from src.schemas.work_day import WorkDayCreate, WorkDayUpdate
from datetime import date


class WorkService:
    async def _update_cache(self, cache_key: str, data: List[WorkDayRead], redis_client: Redis):
        dict_data = [x.model_dump_ext() for x in data]
        await redis_client.setex(cache_key, 300, json.dumps(dict_data))  # Сериализуем в JSON

    async def get_week_schedule(self, week: date, uow: IUnitOfWork, user_id: int):
        async with uow:
            res = await uow.work_day.get_week_schedule(week, user_id)
            return res

    async def get_schedule(self, uow: IUnitOfWork, date_filter: date, location_id: id, redis_client: Redis,
                           background_tasks: BackgroundTasks):
        cache_key = f"schedule:date_filter_{date_filter}:location_id_{location_id}"
        cached_schedule = await redis_client.get(cache_key)
        if cached_schedule:
            return json.loads(cached_schedule)
        async with uow:
            schedule_data = await uow.work_day.get_workdays(date_filter=date_filter, location_id=location_id)
            background_tasks.add_task(self._update_cache, cache_key, schedule_data, redis_client)
            return schedule_data

    async def get_schedule_filter(self, uow: IUnitOfWork, filters: WorkDayFilter, date_filter: Optional[date] = None):
        async with uow:
            print(date_filter)
            schedule = await uow.work_day.get_filtered(filters=filters, month_date=date_filter)
            return schedule

    async def get_list_workdays_for_admin(self, uow: IUnitOfWork, date_now: date, location_id: int):
        async with uow:
            res = await uow.work_day.get_workdays_for_admin(date=date_now, location_id=location_id)
            return res

    async def add_employers_to_work(self, uow: IUnitOfWork, workday: WorkDayCreate):
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

    async def update_work_day(self, uow: IUnitOfWork, id: int, data: WorkDayUpdate):
        data = data.model_dump()
        async with uow:
            await uow.work_day.edit_one(id, data)
            await uow.commit()
