from datetime import date

from fastapi import APIRouter
from src.api.dependses import IUnitOfWork, UOWDep
from src.schemas.work_day import WorkDayCreate

from src.services.work_service import WorkService

router = APIRouter(
    tags=['workdays'],
    prefix='/workdays',
)


@router.get('/get_list_workdays')
async def get_list_workdays(
        page: int,
        limit: int,
        uow: UOWDep
):
    workday_service = WorkService()
    list_workdays = await workday_service.get_list_workdays(uow, page, limit)
    return list_workdays


@router.get('/get_workday_by_fio')
async def get_current_workday(
        fio: str,
        page: int,
        limit: int,
        uow: UOWDep
):
    workday_service = WorkService()
    list_workdays = await workday_service.get_list_workdays_for_current_employer(uow, fio, page, limit)
    return list_workdays


@router.get('/get_workday_by_date')
async def get_current_workday(
        target_date: date,
        page: int,
        limit: int,
        uow: UOWDep
):
    workday_service = WorkService()
    list_workdays = await workday_service.get_list_workdays_for_current_day(uow, target_date, page, limit)
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
async def delete_workday(uow: UOWDep,fio:str):
    workday_service = WorkService()
    await workday_service.delete_work_day(uow, fio)

