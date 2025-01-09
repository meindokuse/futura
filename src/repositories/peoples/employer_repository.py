from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Employer


class EmployerRepository(SQLAlchemyRepository):
    model = Employer

    async def find_one_with_work_days(self,fio: str):
        result = await self.session.execute(
            select(self.model)
            .options(selectinload(Employer.work_days))
            .filter_by(fio=fio)
        )
        return result.scalar_one_or_none()


