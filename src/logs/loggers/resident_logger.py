from datetime import datetime
from typing import Any

from src.data.unitofwork import UnitOfWork
from src.logs.logger import ILogger
from src.schemas.items import EventCreate, EventUpdate, EventRead
from src.schemas.logs import LogsCreate
from src.schemas.peoples import ResidentUpdate, ResidentRead, ResidentCreate
from src.utils.log_enum import LogType, LogAction


class ResidentLogger(ILogger):

    async def log_for_delete(self, id: int):
        resident = await self.uow.residents.get_current_resident(id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.RESIDENTS,
            action=LogAction.DELETED,
            object_action=f'ФИО удаленного постоянного клиента - "{resident.fio.capitalize()}"'
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_update(self, id: int, data):
        data: ResidentUpdate

        old_data = await self.uow.residents.get_current_resident(id)
        updates = self._get_string_update(data, old_data)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.RESIDENTS,
            action=LogAction.UPDATED,
            object_action=updates
        )

        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_create(self, data):
        data: ResidentCreate
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.RESIDENTS,
            action=LogAction.CREATED,
            object_action=f'ФИО добавленного постоянного клиента - "{data.fio.capitalize()}"'
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    def _get_string_update(self, data: ResidentUpdate, old_resident: ResidentRead):
        changes = []
        changes.append(f"ФИО редактируемого - {old_resident.fio.capitalize()}")

        # Обычные поля
        if data.fio is not None and data.fio != old_resident.fio:
            changes.append(f"ФИО: {old_resident.fio} -> {data.fio}")

        if data.description is not None and data.description != old_resident.description:
            changes.append(f"Изменено описание")

        if data.discount_value is not None and data.discount_value != old_resident.discount_value:
            changes.append(f"Размер скидки: {old_resident.discount_value} -> {data.discount_value}")
        return "\n".join(changes) if changes else "Изменений нет"



