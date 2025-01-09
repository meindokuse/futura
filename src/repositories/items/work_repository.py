from datetime import date

from sqlalchemy import func, select

from src.data.repository import SQLAlchemyRepository
from src.models.items import EmployerInWorkDay


class WorkRepository(SQLAlchemyRepository):
    model = EmployerInWorkDay

    async def get_employers_by_date(self, target_date: date):
        stmt = select(EmployerInWorkDay).where(func.date(EmployerInWorkDay.work_time) == target_date)
        result = await self.session.execute(stmt)
        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready
