from src.data.unitofwork import IUnitOfWork
from src.logs.loggers.resident_logger import ResidentLogger
from src.schemas.logs import LogsCreate
from src.schemas.peoples import ResidentCreate, ResidentUpdate


class ResidentsService:
    async def get_list_residents(self, uow: IUnitOfWork, page: int, limit: int):
        async with uow:
            list_residents = await uow.residents.find_all_residents(page=page, limit=limit)
            return list_residents

    async def get_residents_with_filter(self, uow: IUnitOfWork, fio: str, page: int, limit: int):
        async with uow:
            residents = await uow.residents.find_with_filter(page=page, limit=limit, fio=fio)

        return residents

    async def get_current_resident(self, uow: IUnitOfWork, id: int):
        async with uow:
            resident = await uow.residents.get_current_resident(id=id)
            return resident

    # ДЛЯ АДМИНА
    async def add_resident(self, uow: IUnitOfWork, resident: ResidentCreate, admin_id: int):
        dict_resident = resident.model_dump()
        async with uow:
            await ResidentLogger(admin_id, uow).log_for_create(resident)
            id = await uow.residents.add_one(data=dict_resident)
            await uow.commit()
            return id

    async def delete_resident(self, uow: IUnitOfWork, id: int,admin_id: int):
        async with uow:
            await ResidentLogger(admin_id, uow).log_for_delete(id)

            await uow.residents.delete_one(id=id)
            await uow.commit()

    async def update_resident(self, uow: IUnitOfWork, resident: ResidentUpdate, id: int,admin_id: int):
        dict_resident = resident.model_dump()
        async with uow:
            await ResidentLogger(admin_id, uow).log_for_update(id,resident)
            await uow.residents.edit_one(id=id, data=dict_resident)
            await uow.commit()
            return id
