from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.schemas.items import CardCreate


class CardService:

    async def get_list_cards(self, uow: IUnitOfWork, page: int, limit: int,
                                title: Optional[str], location_id: Optional[int]):
        async with uow:
            manuals = await uow.card.find_cards_with_filter(page,limit,title, location_id)
            return manuals

    async def add_card(self, uow: IUnitOfWork, product: CardCreate):
        data = product.model_dump()
        async with uow:
            id = await uow.card.add_one(data)
            await uow.commit()
            return id

    async def delete_card(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.card.delete_one(id=id)
            await uow.commit()
