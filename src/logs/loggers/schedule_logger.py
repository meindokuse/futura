from datetime import datetime
from typing import Any

from src.data.unitofwork import UnitOfWork
from src.logs.logger import ILogger
from src.schemas.items import EventCreate, EventUpdate, EventRead, WorkDayLogsRead
from src.schemas.logs import LogsCreate
from src.schemas.work_day import WorkDayUpdate, WorkDayCreate
from src.utils.log_enum import LogType, LogAction


class ScheduleLogger(ILogger):
    location_mapper = {
        1: 'Проспект Мира',
        2: 'Страстной',
        3: 'Никольская'
    }

    async def log_for_delete(self, id: int):
        shift = await self.uow.work_day.get_current_shift(id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.SCHEDULE,
            action=LogAction.DELETED,
            object_action=f'Смену №{shift.number_work} для {shift.employer_fio}\nДата смены {shift.work_date}',
            location_id=shift.location_id
        )
        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_update(self, id: int, data):
        data: WorkDayUpdate
        employee = await self.uow.employers.get_employee_for_logs(data.employer_id)
        old_shift = await self.uow.work_day.get_current_shift(id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.SCHEDULE,
            action=LogAction.UPDATED,
            object_action=f'Заменил {old_shift.employer_fio.capitalize()} на {employee.fio.capitalize()}\nСмена №{old_shift.number_work}\nДата смены {old_shift.work_date}',
            location_id=old_shift.location_id
        )

        await self.uow.logs.add_one(log_entry.model_dump())

    async def log_for_create(self, data):
        data: WorkDayCreate
        employee = await self.uow.employers.get_employee_for_logs(data.employer_id)
        log_entry = LogsCreate(
            admin_id=self.admin_id,
            type=LogType.SCHEDULE,
            action=LogAction.CREATED,
            object_action=f'Смена №{data.number_work} для {employee.fio}\n Дата смены {data.work_date}',
            location_id=data.location_id
        )
        await self.uow.logs.add_one(log_entry.model_dump())
