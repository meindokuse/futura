from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.items import Location
from src.models.peoples import Employer


class EmployerRepository(SQLAlchemyRepository):
    model = Employer

    async def get_employees(
            self,
            page: int,
            limit: int,
            sort_by: str = "fio",
            sort_order: str = "asc",
            filter_by: dict = None,
    ):
        filter_by = filter_by or {}

        if not hasattr(Employer, sort_by):
            raise AttributeError(f"Model Employer has no attribute '{sort_by}'.")

        order_by = getattr(Employer, sort_by).desc() if sort_order.lower() == "desc" else getattr(Employer,
                                                                                                  sort_by).asc()
        start = (page - 1) * limit

        filters = [
            getattr(Employer, key) == value
            for key, value in filter_by.items()
            if hasattr(Employer, key)
        ]

        stmt = (
            select(Employer)
            .options(selectinload(Employer.location))  # Явная загрузка location
            .where(*filters)
            .order_by(order_by)
            .offset(start)
            .limit(limit)
        )

        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def get_current_employer(self, id: int):
        stmt = (
            select(Employer)
            .join(Location, Employer.location_id == Location.id)
            .where(Employer.id == id)
        )

        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res.to_read_model()
