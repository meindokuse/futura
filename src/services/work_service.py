from datetime import datetime
from typing import Optional

from src.data.unitofwork import IUnitOfWork

from src.schemas.items import EmployerInWorkDayCreate


class WorkService:
    async def get_list_employers_to_work(self, uow: IUnitOfWork, work_day: datetime.date):
        async with uow:
            a = 1
            # TO DO

    async def change_status_work(self, uow: IUnitOfWork, status_work: int, fio: Optional[str] = None,
                                 id: Optional[int] = None):
        async with uow:
            if fio is None:
                await uow.work_day.edit_one(id=id, data={"status": status_work})
            else:
                employer = await uow.employers.find_one(fio=fio)
                id = employer.id
                await uow.work_day.edit_one(id=id, data={"status": status_work})

    async def add_employers_to_work(self, uow: IUnitOfWork, employer_in_work: EmployerInWorkDayCreate):
        data = employer_in_work.model_dump()
        async with uow:
            await uow.work_day.add_one(data)
