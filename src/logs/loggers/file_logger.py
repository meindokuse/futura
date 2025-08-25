from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.schemas.logs import LogsCreate
from src.utils.log_enum import LogType, LogAction, LogRelationObject


class FileLogger:
    def __init__(self, admin_id: int, uow: IUnitOfWork):
        self.admin_id = admin_id
        self.uow = uow

    async def log_for_manual(self, manual_id: int):
        async with self.uow:
            manual = await self.uow.card.find_one(id=manual_id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.MANUAL,
            action=LogAction.UPDATED,
            object_action=f'Изменил файл для методички с названием {manual.title}',
            location_id=manual.location_id,
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_resident(self,resident_id: int):
        async with self.uow:
            resident = await self.uow.residents.find_one(id=resident_id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.RESIDENTS,
            action=LogAction.UPDATED,
            object_action=f'Изменил фото для постоянного клиента с ФИО: {resident.fio}',
        )
        await self.uow.logs.add_one(log_entry.model_dump())



