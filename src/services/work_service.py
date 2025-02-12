from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from src.data.unitofwork import IUnitOfWork

from src.schemas.work_day import WorkDayCreate


class WorkService:

    async def get_list_workdays(self, uow: IUnitOfWork, page: int, limit: int, location_name: str):
        async with uow:
            res = await uow.work_day.get_workdays(page=page, limit=limit, location_name=location_name)
            return res

    async def get_list_workdays_for_current_employer(self, uow: IUnitOfWork, fio: str, page: int, limit: int,
                                                     location_name: str):
        async with uow:
            res = await uow.work_day.find_all(page=page, limit=limit, employer_fio=fio, location_name=location_name)
            return res

    async def get_list_workdays_for_current_day(self, uow: IUnitOfWork, work_day: datetime.date, page: int, limit: int,
                                                location_name: str):
        async with uow:
            res = await uow.work_day.get_workdays_by_date(work_day, page, limit, location_name=location_name)
            return res

    # async def change_status_work(self, uow: IUnitOfWork, status_work: int, fio: Optional[str] = None,
    #                              id: Optional[int] = None):
    #     async with uow:
    #         if fio is None:
    #             await uow.work_day.edit_one(id=id, data={"status": status_work})
    #         else:
    #             employer = await uow.employers.find_one(fio=fio)
    #             id = employer.id
    #             await uow.work_day.edit_one(id=id, data={"status": status_work})

    async def add_employers_to_work(self, uow: IUnitOfWork, employer_in_work: WorkDayCreate):
        if employer_in_work.work_time.tzinfo is not None:
            employer_in_work.work_time = employer_in_work.work_time.replace(tzinfo=None)
            raise HTTPException(status_code=500)
        data = employer_in_work.model_dump()
        async with uow:
            await uow.work_day.add_one(data)
            await uow.commit()

    async def delete_work_day(self, uow: IUnitOfWork, fio: str):
        async with uow:
            await uow.work_day.delete_one(fio=fio)
            await uow.commit()
