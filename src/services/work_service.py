import json
from typing import Optional, List

from fastapi import Depends
from redis.asyncio import Redis
from fastapi import BackgroundTasks

from src.celery.tasks.redis_update_task import update_schedule_cache_after_add, update_schedule_cache_with_data
from src.data.unitofwork import IUnitOfWork
from src.db.async_cache import get_redis
from src.logs.loggers.schedule_logger import ScheduleLogger
from src.schemas.items import WorkDayRead, WorkDayFilter

from src.schemas.work_day import WorkDayCreate, WorkDayUpdate
from datetime import date
from redis.asyncio import ConnectionError


class WorkService:
    async def get_week_schedule(self, week: date, uow: IUnitOfWork, user_id: int):
        async with uow:
            res = await uow.work_day.get_week_schedule(week, user_id)
            return res

    async def get_schedule_filter(self, redis: Redis, uow: IUnitOfWork, filters: WorkDayFilter,
                                  date_filter: Optional[date] = None,
                                  ):
        year = date_filter.year if date_filter else date.today().year
        month = date_filter.month if date_filter else date.today().month
        location_id = filters.location_id
        key = f"schedule:{year}-{month}:{location_id}"
        try:
            cached_data = await redis.get(key)
            if cached_data and not filters.employer_fio and not filters.work_type:
                print(f"Cache hit for {key}")
                cached_list = json.loads(cached_data)

                return cached_list
        except ConnectionError as e:
            print(f"Redis connection error: {e}")
        async with uow:
            schedule = await uow.work_day.get_filtered(filters=filters, month_date=date_filter)
            if not filters.employer_fio and not filters.work_type:
                data = [x.model_dump() for x in schedule]
                update_schedule_cache_with_data.delay(year, month, location_id, data)
            return schedule

    async def get_list_workdays_for_admin(self, uow: IUnitOfWork, date_now: date, location_id: int):
        async with uow:
            res = await uow.work_day.get_workdays_for_admin(date=date_now, location_id=location_id)
            return res

    async def add_employers_to_work(self, uow: IUnitOfWork, workday: WorkDayCreate, admin_id: int):
        data = workday.model_dump()
        async with uow:
            await ScheduleLogger(admin_id, uow).log_for_create(workday)
            await uow.work_day.add_one(data=data)
            await uow.commit()

        year, month = workday.work_date.year, workday.work_date.month
        update_schedule_cache_after_add.delay(year, month, workday.location_id)

    async def add_list_workdays(self, uow: IUnitOfWork, workdays: List[WorkDayCreate]):
        data = [x.model_dump() for x in workdays]
        async with uow:
            await uow.work_day.add_all(data_list=data)
            await uow.commit()

    async def delete_work_day(self, uow: IUnitOfWork, id: int, admin_id: int):
        async with uow:
            await ScheduleLogger(admin_id, uow).log_for_delete(id)
            await uow.work_day.delete_one(id=id)
            await uow.commit()

    async def update_work_day(self, uow: IUnitOfWork, id: int, data: WorkDayUpdate, admin_id: int):
        data_dict = data.model_dump()
        async with uow:
            await ScheduleLogger(admin_id, uow).log_for_update(id, data)
            await uow.work_day.edit_one(id, data_dict)
            await uow.commit()
