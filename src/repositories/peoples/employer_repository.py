from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Employer


class EmployerRepository(SQLAlchemyRepository):
    model = Employer

    # async def find_one_with_work_days(self,fio: str):
    #     result = await self.session.execute(
    #         select(self.model)
    #         .options(selectinload(Employer.work_days))
    #         .filter_by(fio=fio)
    #     )
    #     res = result.scalar_one_or_none()
    #     if res:
    #         return res.to_read_model_with_work_days()
    #     return None

    async def get_employees(
            self,
            page: int,  # Смещение для пагинации
            limit: int,  # Лимит записей на страницу
            sort_by: str = "fio",  # Поле для сортировки (по умолчанию "name")
            sort_order: str = "asc",  # Порядок сортировки ("asc" или "desc")
            **filter_by,  # Фильтры в виде словаря
    ):
        if sort_order.lower() == "desc":
            order_by = getattr(self.model, sort_by).desc()
        else:
            order_by = getattr(self.model, sort_by).asc()

        start = (page - 1) * limit

        stmt = select(self.model).filter_by(**filter_by).order_by(order_by)

        stmt = stmt.offset(start).limit(limit)

        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
