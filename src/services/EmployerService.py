from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.schemas.peoples import EmployerCreate


class EmployerService:
    async def get_list_employer(self, uow: IUnitOfWork, page: int, limit: int):
        async with uow:
            list_residents = await uow.residents.find_all(page=page, limit=limit)
            return list_residents

    async def get_current_employer(self, uow: IUnitOfWork, fio: str):
        async with uow:
            resident = await uow.residents.find_one(fio=fio)
            return resident

    async def get_list_work_days_for_current_employer(self, uow: IUnitOfWork, fio: Optional[str] = None,
                                                      id: Optional[int] = None):
        async with uow:
            if fio is None:
                employer = await uow.employers.find_one(id=id)
            else:
                employer = await uow.employers.find_one(fio=fio)

            return employer.work_days

    # ДЛЯ АДМИНА
    async def add_employer(self, uow: IUnitOfWork, employer: EmployerCreate):
        data = employer.model_dump()
        async with uow:
            await uow.residents.add_one(employer)
