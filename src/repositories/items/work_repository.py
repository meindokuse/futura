from datetime import date, datetime, timedelta

from sqlalchemy import func, select

from src.data.repository import SQLAlchemyRepository
from src.models.items import WorkDay, Location
from src.models.peoples import Employer


class WorkRepository(SQLAlchemyRepository):
    model = WorkDay

    async def get_workdays_by_date(self, target_date: date, page: int, limit: int, **filter_by):
        offset = (page - 1) * limit

        # Диапазон дат
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)

        stmt = (
            select(self.model)
            .join(Employer, WorkDay.employer_id == Employer.id)  # Соединяем с Employer
            .join(Location, WorkDay.location_id == Location.id)  # Соединяем с Location
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
            .join(Employer, WorkDay.employer_id == Employer.id)  # Соединяем с Employer
            .join(Location, WorkDay.location_id == Location.id)  # Соединяем с Location
            .filter_by(**filter_by)  # Применяем дополнительные фильтры
            .where(WorkDay.work_time >= today)
            .order_by(WorkDay.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_workdays_by_fio(self, fio: str, page: int, limit: int,location_id:int):
        offset = (page - 1) * limit

        stmt = (
            select(WorkDay)
            .join(Employer, WorkDay.employer_id == Employer.id)  # Соединяем с Employer
            .join(Location, WorkDay.location_id == Location.id)  # Соединяем с Location
            .where(Employer.fio == fio and WorkDay.location_id == location_id)  # Фильтр по ФИО
            .order_by(WorkDay.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready
