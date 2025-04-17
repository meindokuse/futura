from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from src.api.dependses import IUnitOfWork, UOWDep
from src.db.cache import get_redis
from src.models.items import WorkDay
from src.schemas.items import WorkDayFilter
from src.schemas.work_day import WorkDayCreate, WorkDayUpdate

from src.services.work_service import WorkService
from fastapi import BackgroundTasks

router = APIRouter(
    tags=['workdays'],
    prefix='/workdays',
)


# @router.get('/get_list_workdays')
# async def get_list_workdays(
#         back_tasks: BackgroundTasks,
#         location_id: int,
#         page: int,
#         limit: int,
#         uow: UOWDep,
#         date: Optional[date] = None,
#         redis_client: Redis = Depends(get_redis),
# ):
#     filter_by = {"location_id": location_id}
#
#     if date:
#         filter_by["work_type"] = date
#
#     workday_service = WorkService()
#     list_workdays = await workday_service.get_schedule(uow, page, limit, location_id, redis_client, back_tasks)
#     return list_workdays
#
#
# @router.get('/get_workdays_by_fio')
# async def get_current_workdays_by_fio(
#         location_id: int,
#         fio: str,
#         page: int,
#         limit: int,
#         uow: UOWDep
# ):
#     workday_service = WorkService()
#     list_workdays = await workday_service.get_list_workdays_for_current_employer(uow, fio, page, limit, location_id)
#     return list_workdays
#
#
# @router.get('/get_workday_by_date')
# async def get_current_workdays_by_date(
#         location_id: int,
#         target_date: date,
#         page: int,
#         limit: int,
#         uow: UOWDep
# ):
#     workday_service = WorkService()
#     list_workdays = await workday_service.get_list_workdays_for_current_day(uow, target_date, page, limit,
#                                                                             location_id)
#     return list_workdays


@router.get("/get_workday_filter")
async def get_workdays(
        uow: UOWDep,
        date: Optional[date] = None,
        employer_fio: Optional[str] = None,
        location_id: Optional[int] = None,
        work_type: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
):
    workday_service = WorkService()
    filters = WorkDayFilter(
        employer_fio=employer_fio,
        location_id=location_id,
        work_type=work_type.lower() if work_type else None,
        page=page,
        limit=limit
    )

    return await workday_service.get_schedule_filter(uow, filters, date)


@router.post('/add_workday')
async def add_workday(
        workday: WorkDayCreate,
        uow: UOWDep
):
    workday = workday.preprocess()
    workday_service = WorkService()
    await workday_service.add_employers_to_work(uow, workday)


@router.post('/add_list_workdays')
async def add_workdays_list(
        workdays: List[WorkDayCreate],
        uow: UOWDep
):
    workdays = [workday.preprocess() for workday in workdays]
    workday_service = WorkService()
    await workday_service.add_list_workdays(uow, workdays)


@router.delete('/delete_workday')
async def delete_workday(uow: UOWDep, id: int):
    workday_service = WorkService()
    await workday_service.delete_work_day(uow, id)


@router.put('/update_workday')
async def update_workday(
        workday_update: WorkDayUpdate,
        uow: UOWDep,
):
    workday_service = WorkService()
    await workday_service.update_work_day(uow, workday_update.id, workday_update)
