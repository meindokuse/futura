import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from redis.asyncio import Redis

from src.data.unitofwork import IUnitOfWork

from src.schemas.work_day import WorkDayCreate


class WorkService:
    async def _update_cache(self, uow: IUnitOfWork, page: int, limit: int, location_id: int, redis_client: Redis):
        async with uow:
            schedule_data = await uow.work_day.get_workdays(page=page, limit=limit, location_id=location_id)
            await redis_client.setex("schedule", timedelta(hours=24), json.dumps(schedule_data))

    async def get_schedule(self, uow: IUnitOfWork, page: int, limit: int, location_id: id, redis_client: Redis):
        cached_schedule = await redis_client.get("schedule")
        if cached_schedule:
            return json.loads(cached_schedule)
        asyncio.create_task(self._update_cache(uow, page, limit, location_id, redis_client))

        async with uow:
            res = await uow.work_day.get_workdays(page=page, limit=limit, location_id=location_id)
            return res

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

    async def add_employers_to_work(self, uow: IUnitOfWork, employer_in_work: WorkDayCreate):
        if employer_in_work.work_time.tzinfo is not None:
            employer_in_work.work_time = employer_in_work.work_time.replace(tzinfo=None)
            raise HTTPException(status_code=500)
        data = employer_in_work.model_dump()
        async with uow:
            await uow.work_day.add_one(data)
            await uow.commit()

    async def delete_work_day(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.work_day.delete_one(id=id)
            await uow.commit()
