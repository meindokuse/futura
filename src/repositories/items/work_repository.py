from datetime import date, datetime, timedelta
from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.items import WorkDay, Location
from src.models.peoples import Employer
from src.schemas.work_day import WorkDayCreate


class WorkRepository(SQLAlchemyRepository):
    model = WorkDay

    async def get_workdays_by_date(self, target_date: date, page: int, limit: int, **filter_by):
        offset = (page - 1) * limit

        # Диапазон дат
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)

        stmt = (
            select(self.model)
            .options(
                selectinload(WorkDay.employer),  # Загружаем связанный Employer
                selectinload(WorkDay.location),  # Загружаем связанный Location
            )
            .filter_by(**filter_by)  # Применяем дополнительные фильтры
            .where(WorkDay.work_time >= start_datetime, WorkDay.work_time < end_datetime)
            .order_by(WorkDay.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_workdays(self, page: int, limit: int, **filter_by):
        today = date.today()
        offset = (page - 1) * limit

        stmt = (
            select(WorkDay)
            .options(
                selectinload(WorkDay.employer),  # Загружаем связанный Employer
                selectinload(WorkDay.location),  # Загружаем связанный Location
            )
            .filter_by(**filter_by)  # Фильтруем по атрибутам WorkDay
            .where(WorkDay.work_time >= today)  # Дополнительный фильтр
            .order_by(WorkDay.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_workdays_by_fio(self, fio: str, page: int, limit: int, location_id: int):
        offset = (page - 1) * limit

        stmt = (
            select(WorkDay)
            .options(
                selectinload(WorkDay.employer),  # Загружаем связанный Employer
                selectinload(WorkDay.location),  # Загружаем связанный Location
            )
            .where(Employer.fio == fio.lower(), WorkDay.location_id == location_id)  # Фильтр по ФИО и location_id
            .order_by(WorkDay.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def add_list_workdays(self,workdays: List[WorkDayCreate]):
        stmt = select(WorkDay)


