from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.schemas.items import CardCreate


class CardService:

    async def get_list_cards(self, uow: IUnitOfWork, page: int, limit: int,
                                category: Optional[str], location_id: int):
        async with uow:
            if category is None:
                cards = await uow.card.find_all(page=page, limit=limit, location_id=location_id)
            else:
                cards = await uow.card.find_all(page=page, limit=limit, category=category,
                                                      location_id=location_id)
            return cards

    async def add_card(self, uow: IUnitOfWork, product: CardCreate):
        data = product.model_dump()
        async with uow:
            await uow.card.add_one(data)
            await uow.commit()

    async def delete_card(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.card.delete_one(id=id)
            await uow.commit()
