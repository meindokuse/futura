from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Residents


class ResidentsRepository(SQLAlchemyRepository):
    model = Residents

    async def find_with_filter(
            self,
            page: int,  # Смещение для пагинации
            limit: int,  # Лимит записей на страницу
            fio: str,  # ФИО для фильтрации
            **fiter_kwargs
    ):
        start = (page - 1) * limit

        # Используем func.lower для приведения к lowercase
        stmt = (select(self.model)
        .filter_by(**fiter_kwargs).where(
            func.lower(self.model.fio).ilike(f"%{fio.lower()}%")
        ))

        stmt = stmt.offset(start).limit(limit)

        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_all_residents(self, page: int, limit: int):
        start = (page - 1) * limit
        stmt = select(Residents)
        stmt = stmt.offset(start).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model_for_cards() for row in res.all()]
        return res

    async def get_current_resident(self, id: int):
        stmt = (
            select(Residents)
            .where(Residents.id == id)
        )
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            return res.to_read_model()
        return None