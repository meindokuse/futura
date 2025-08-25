from datetime import datetime
from typing import Any

from src.data.unitofwork import UnitOfWork
from src.logs.logger import ILogger
from src.schemas.items import EventCreate, EventUpdate, EventRead
from src.schemas.logs import LogsCreate
from src.utils.log_enum import LogType, LogAction


class EventLogger(ILogger):
    location_mapper = {
        1: 'Проспект Мира',
        2: 'Страстной',
        3: 'Никольская'
    }

    async def log_for_delete(self, id: int):
        event = await self.uow.event.get_event_for_logs(id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.EVENTS,
            action=LogAction.DELETED,
            object_action=f'Заголовок удаленного события - "{event.name}"',
            location_id=event.location_id,
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_update(self, id: int, data):
        data: EventUpdate
        print(data)

        old_event = await self.uow.event.get_event_for_logs(id)
        updates = self._get_string_update(data, old_event)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.EVENTS,
            action=LogAction.UPDATED,
            object_action=updates,
            location_id=old_event.location_id,
        )

        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_create(self, data):
        data: EventCreate
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.EVENTS,
            action=LogAction.CREATED,
            object_action=f'Заголовок добавленного события - "{data.name}"',
            location_id=data.location_id,
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    def _get_string_update(self, data: EventUpdate, old_event: EventRead):
        changes = []
        changes.append(f"Заголовок редактируемого события - {old_event.name}")

        # Обычные поля
        if data.name is not None and data.name != old_event.name:
            changes.append(f"Заголовок: {old_event.name} -> {data.name}")

        if data.date_start is not None and data.date_start != old_event.date_start:
            print(data.date_start)
            old_date = self._format_val(old_event.date_start)
            new_date = self._format_val(data.date_start)
            changes.append(f"Дата начала: {old_date} -> {new_date}")

        if data.description is not None and data.description != old_event.description:
            changes.append(f"Изменено описание")

        # Особый случай для локации

        old_location_name = self.location_mapper.get(old_event.location_id, f"Общее событие")
        new_location_name = self.location_mapper.get(data.location_id, f"Сделал событие общим")
        if data.location_id != old_event.location_id:
            changes.append(f"Локация: {old_location_name} -> {new_location_name}")

        return "\n".join(changes) if changes else "Изменений нет"

    def _format_val(self, value: Any) -> str:
        if isinstance(value, datetime):
            return value.strftime("%d.%m.%Y %H:%M")
        elif isinstance(value, str):
            return f'"{value}"'
        return str(value)
