from datetime import date

from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from src.api.dependses import IUnitOfWork, UOWDep
from src.db.cache import get_redis
from src.schemas.work_day import WorkDayCreate

from src.services.work_service import WorkService

router = APIRouter(
    tags=['workdays'],
    prefix='/workdays',
)


@router.get('/{location_name}/get_list_workdays')
async def get_list_workdays(
        location_name: str,
        page: int,
        limit: int,
        uow: UOWDep,
        redis_client: Redis = Depends(get_redis)
):
    workday_service = WorkService()
    list_workdays = await workday_service.get_list_workdays(uow, page, limit, location_name,redis_client)
    return list_workdays


@router.get('/{location_name}/get_workdays_by_fio')
async def get_current_workdays_by_fio(
        location_name: str,
        fio: str,
        page: int,
        limit: int,
        uow: UOWDep
):
    workday_service = WorkService()
    list_workdays = await workday_service.get_list_workdays_for_current_employer(uow, fio, page, limit, location_name)
    return list_workdays


@router.get('/{location_name}/get_workday_by_date')
async def get_current_workdays_by_date(
        location_name: str,
        target_date: date,
        page: int,
        limit: int,
        uow: UOWDep
):
    workday_service = WorkService()
    list_workdays = await workday_service.get_list_workdays_for_current_day(uow, target_date, page, limit,
                                                                            location_name)
    return list_workdays


@router.post('/add_workday')
async def add_workday(
        workday: WorkDayCreate,
        uow: UOWDep
):
    workday = workday.preprocess()
    workday_service = WorkService()
    await workday_service.add_employers_to_work(uow, workday)


@router.delete('/delete_workday')
async def delete_workday(uow: UOWDep, fio: str):
    workday_service = WorkService()
    await workday_service.delete_work_day(uow, fio)
