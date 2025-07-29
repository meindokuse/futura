from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from src.api.dependses import IUnitOfWork, UOWDep
from src.schemas.items import WorkDayFilter
from src.schemas.work_day import WorkDayCreate, WorkDayUpdate
from src.services.work_service import WorkService
from src.utils.jwt_tokens import user_dep

router = APIRouter(
    tags=['workdays'],
    prefix='/workdays',
)


@router.get("/get_workday_filter")
async def get_workdays(
        uow: UOWDep,
        location_id: int,
        date_now: Optional[date] = None,
        employer_fio: Optional[str] = None,
        work_type: Optional[str] = None,
):
    workday_service = WorkService()
    filters = WorkDayFilter(
        employer_fio=employer_fio,
        location_id=location_id,
        work_type=work_type.lower() if work_type else None,
    )

    return await workday_service.get_schedule_filter(uow, filters, date_now)


@router.get('/schedule_admin')
async def get_schedule_admin(date_now: date, location_id: int, uow: UOWDep):
    workday_service = WorkService()
    return await workday_service.get_list_workdays_for_admin(uow, date_now, location_id)


@router.get('/get_week_schedule')
async def get_week_schedule(week: date, uow: UOWDep, user: user_dep):
    workday_service = WorkService()
    return await workday_service.get_week_schedule(week, uow, int(user.id))


@router.get('/get_week_schedule_employer')
async def get_week_schedule(week: date, uow: UOWDep, id: int):
    workday_service = WorkService()
    return await workday_service.get_week_schedule(week, uow, id)


@router.post('/admin/add_workday')
async def add_workday(
        workday: WorkDayCreate,
        uow: UOWDep
):
    workday_service = WorkService()
    await workday_service.add_employers_to_work(uow, workday)


@router.post('/admin/add_list_workdays')
async def add_workdays_list(
        workdays: List[WorkDayCreate],
        uow: UOWDep
):
    workdays = [workday.preprocess() for workday in workdays]
    workday_service = WorkService()
    await workday_service.add_list_workdays(uow, workdays)


@router.delete('/admin/delete_workday')
async def delete_workday(uow: UOWDep, id: int):
    workday_service = WorkService()
    await workday_service.delete_work_day(uow, id)


@router.put('/admin/{workday_id}/update_workday')
async def update_workday(
        workday_update: WorkDayUpdate,
        workday_id:int,
        uow: UOWDep,
):
    workday_service = WorkService()
    await workday_service.update_work_day(uow, workday_id, workday_update)
