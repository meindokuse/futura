from datetime import datetime
from typing import Any

from src.data.unitofwork import UnitOfWork
from src.logs.logger import ILogger
from src.schemas.items import EventCreate, EventUpdate, EventRead, CardUpdate, CardRead
from src.schemas.logs import LogsCreate
from src.utils.log_enum import LogType, LogAction


class ManualLogger(ILogger):
    location_mapper = {
        1: 'Проспект Мира',
        2: 'Страстной',
        3: 'Никольская'
    }

    async def log_for_delete(self, id: int):
        manual = await self.uow.card.find_one(id=id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.MANUAL,
            action=LogAction.DELETED,
            object_action=f'Заголовок удаленной методички - "{manual.title}"',
            location_id=manual.location_id,

        )
        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_update(self, id: int, data):
        data: CardUpdate

        old_manual = await self.uow.card.find_one(id=id)
        updates = self._get_string_update(data, old_manual)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.MANUAL,
            action=LogAction.UPDATED,
            object_action=updates,
            location_id=old_manual.location_id,
        )

        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_create(self, data):
        data: EventCreate
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.MANUAL,
            action=LogAction.CREATED,
            object_action=f'Заголовок добавленной методички - "{data.title}"',
            location_id=data.location_id,
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    def _get_string_update(self, data: CardUpdate, old_manual: CardRead):
        changes = []
        changes.append(f"Заголовок редактируемой методички - {old_manual.title}")

        # Обычные поля
        if data.title is not None and data.title != old_manual.title:
            changes.append(f"Заголовок: {old_manual.title} -> {data.title}")

        if data.description is not None and data.description != old_manual.description:
            changes.append(f"Изменено описание")

        # Особый случай для локации

        old_location_name = self.location_mapper.get(old_manual.location_id, f"Общая методичка")
        new_location_name = self.location_mapper.get(data.location_id, f"Сделал методичку общей")
        if data.location_id != old_manual.location_id:
            changes.append(f"Локация: {old_location_name} -> {new_location_name}")

        return "\n".join(changes) if changes else "Изменений нет"

