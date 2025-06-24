from typing import Optional

from sqlalchemy import select

from src.data.repository import SQLAlchemyRepository
from src.models.items import Card


class CardRepository(SQLAlchemyRepository):
    model = Card

    async def find_cards_with_filter(
            self,
            page: int,
            limit: int,
            title: Optional[str] = None,
            location_id: Optional[int] = None
    ):
        # Основной запрос для данных
        stmt = select(self.model).order_by(self.model.title.asc())


        if title:
            stmt = stmt.where(self.model.title.ilike(f'%{title}%'))

        stmt = stmt.where(
            (self.model.location_id == location_id)
        )

        stmt = stmt.offset((page - 1) * limit).limit(limit)

        # Выполняем запросы
        cards_result = await self.session.execute(stmt)
        cards = cards_result.scalars().all()
        return [c.to_read_model() for c in cards] if cards else []
