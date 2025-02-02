from src.data.unitofwork import IUnitOfWork
from src.schemas.peoples import ResidentCreate


class ResidentsService:
    async def get_list_residents(self, uow: IUnitOfWork, page: int, limit: int):
        async with uow:
            list_residents = await uow.residents.find_all(page=page, limit=limit)
            return list_residents

    async def get_current_residents(self, uow: IUnitOfWork, fio: str, page: int, limit: int):
        async with uow:
            residents = await uow.residents.find_with_filter(page=page, limit=limit, fio=fio)
            return residents

    # ДЛЯ АДМИНА
    async def add_resident(self, uow: IUnitOfWork, resident: ResidentCreate):
        dict_resident = resident.model_dump()
        async with uow:
            await uow.residents.add_one(data=dict_resident)
            await uow.commit()

    async def delete_resident(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.residents.delete_one(id=id)
            await uow.commit()
