from datetime import date

from sqlalchemy import func, select

from src.data.repository import SQLAlchemyRepository
from src.models.items import WorkDay


class WorkRepository(SQLAlchemyRepository):
    model = WorkDay

    async def get_workdays_by_date(self, target_date: date, page: int, limit: int):
        offset = (page - 1) * limit

        stmt = (
            select(WorkDay)
            .where(func.date(WorkDay.work_time) == target_date)
            .order_by(WorkDay.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_workdays(self, page: int, limit: int):
        today = date.today()

        offset = (page - 1) * limit

        stmt = (
            select(self.model)
            .where(self.model.work_time >= today)
            .order_by(self.model.work_time.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready
