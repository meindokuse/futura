from datetime import date, datetime, timedelta
from typing import List, cast, Optional
from sqlalchemy import func, select, and_, Date, extract, delete
from sqlalchemy.orm import selectinload, joinedload
from src.data.repository import SQLAlchemyRepository
from src.models.items import WorkDay, Location
from src.models.peoples import Employer
from src.schemas.items import WorkDayFilter
from src.schemas.work_day import WorkDayCreate
from datetime import date, datetime
from typing import Optional


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
    async def get_current_shift(self,id:int):
        stmt = (
            select(self.model)
            .options(
                selectinload(WorkDay.employer),  # Загружаем связанный Employer
            )
            .where(WorkDay.id == id)
        )

        result = await self.session.execute(stmt)
        shift = result.scalars().first()
        return shift.read_for_logs() if shift else None
    async def get_workdays(self, date_now: date, **filter_by):
        # Получаем год и месяц из date_now
        year = date_now.year
        month = date_now.month

        # Создаем диапазон дат для всего месяца
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year, month, 31)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)

        stmt = (
            select(WorkDay)
            .options(
                selectinload(WorkDay.employer),
            )
            .filter_by(**filter_by)
            .where(WorkDay.work_date >= first_day, WorkDay.work_date <= last_day)
            .order_by(WorkDay.work_date.asc(), WorkDay.work_time.asc())
        )

        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_workdays_for_admin(self, date: date, location_id: int):

        stmt = (
            select(WorkDay)
            .options(
                selectinload(WorkDay.employer),
            )
            .where(WorkDay.work_date == date, WorkDay.location_id == location_id)
        )
        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_filtered(self, filters: WorkDayFilter, month_date: date):
        """
        Получает рабочие дни за указанный месяц с фильтрацией по ФИО работника

        :param filters: Фильтры (только employer_fio)
        :param month_date: Дата, по которой определяется месяц (год и месяц)
        :return: Список рабочих дней, отсортированный по ФИО работника
        """
        # Определяем границы месяца
        year = month_date.year
        month = month_date.month
        first_day = date(year, month, 1)
        last_day = date(year, month + 1, 1) - timedelta(days=1) if month != 12 else date(year, 12, 31)

        # Создаем базовый запрос с JOIN к employer
        stmt = (
            select(WorkDay)
            .join(WorkDay.employer)  # Добавляем JOIN к таблице employers
            .options(
                selectinload(WorkDay.employer),
                selectinload(WorkDay.location)
            )
            .where(
                WorkDay.work_date >= first_day,
                WorkDay.work_date <= last_day
            )
        )

        # Фильтр по ФИО работника (если указан)
        if filters.employer_fio:
            stmt = stmt.where(Employer.fio.ilike(f"%{filters.employer_fio}%"))
        if filters.location_id:
            stmt = stmt.where(WorkDay.location_id == filters.location_id)
        if filters.work_type:
            stmt = stmt.where(Employer.work_type == filters.work_type)

        # Сортировка по ФИО работника (теперь employer доступен через JOIN)
        stmt = stmt.order_by(Employer.fio.asc())

        if filters.limit and filters.limit != 0:
            stmt = stmt.offset(filters.page).limit(filters.limit)

        result = await self.session.execute(stmt)
        return [wd.to_read_model() for wd in result.scalars().all()]

    async def get_week_schedule(self, week: date, user_id: int):
        delta_date = week + timedelta(days=7)
        stmt = select(self.model).options(
            joinedload(self.model.location)
        )
        stmt = stmt.where(self.model.work_date >= week, self.model.work_date <= delta_date,
                          self.model.employer_id == user_id)
        result = await self.session.execute(stmt)
        return [wd.to_read_for_profile() for wd in result.scalars().all()]

