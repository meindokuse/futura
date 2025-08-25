from datetime import datetime
from typing import Any

from src.data.unitofwork import UnitOfWork
from src.logs.logger import ILogger
from src.schemas.items import EventCreate, EventUpdate, EventRead
from src.schemas.logs import LogsCreate
from src.schemas.peoples import EmployerUpdateAdmin, EmployerRead, EmployerCreate
from src.utils.log_enum import LogType, LogAction


class EmployeeLogger(ILogger):
    location_mapper = {
        1: 'Проспект Мира',
        2: 'Страстной',
        3: 'Никольская'
    }

    async def log_for_delete(self, id: int):
        employee = await self.uow.employers.get_employee_for_logs(id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.EMPLOYEE,
            action=LogAction.DELETED,
            object_action=f'ФИО удаленного сотрудника - "{employee.fio}"',
            location_id=employee.location_id,
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_update(self, id: int, data):
        data_update = EmployerUpdateAdmin(
            is_admin=data.get('is_admin'),
            work_type=data.get('work_type'),
            location_id=data.get('location_id'),
        )


        old_employee = await self.uow.employers.get_employee_for_logs(id)
        updates = self._get_string_update(data_update, old_employee)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.EMPLOYEE,
            action=LogAction.UPDATED,
            object_action=updates,
            location_id=old_employee.location_id,
        )

        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_create(self, data):
        data: EmployerCreate
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.EMPLOYEE,
            action=LogAction.CREATED,
            object_action=f'ФИО добавленного сотрудника - "{data.fio}"',
            location_id=data.location_id,
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    def _get_string_update(self, data: EmployerUpdateAdmin, old_employee: EmployerRead):
        changes = []
        changes.append(f'ФИО редактируемого сотрудника {old_employee.fio}')

        # Обычные поля
        if data.work_type is not None and data.work_type != old_employee.work_type:
            changes.append(f"Должность: {old_employee.work_type} -> {data.work_type}")

        if data.is_admin is not None and data.is_admin != old_employee.is_admin:
            changes.append(self._format_is_admin(data.is_admin))

        # Особый случай для локации
        if data.location_id is not None:
            old_location = self.location_mapper.get(old_employee.location_id, f"Unknown ({data.location_id})")
            new_location = self.location_mapper.get(data.location_id, f"Unknown ({data.location_id})")

            # Нормализуем строки перед сравнением
            old_normalized = old_location.strip().replace('  ', ' ') if old_location else ''
            new_normalized = new_location.strip().replace('  ', ' ') if new_location else ''

            if old_normalized != new_normalized:
                changes.append(f"Локация: {old_location} -> {new_location}")
        return "\n".join(changes) if changes else "Изменений нет"

    def _format_is_admin(self, new_is_admin: bool):
        return 'Выдал права администратора' if new_is_admin == True else 'Отключил права администратора'
