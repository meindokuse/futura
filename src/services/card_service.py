from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.logs.loggers.manuals_logger import ManualLogger
from src.models.items import LogType, LogAction
from src.schemas.items import CardCreate, CardUpdate
from src.schemas.logs import LogsCreate


class CardService:

    async def get_list_cards(self, uow: IUnitOfWork, page: int, limit: int,
                             title: Optional[str], location_id: Optional[int]):
        async with uow:
            manuals = await uow.card.find_cards_with_filter(page, limit, title, location_id)
            return manuals

    async def add_card(self, uow: IUnitOfWork, product: CardCreate, admin_id: int):
        data = product.model_dump()
        async with uow:
            await ManualLogger(admin_id, uow).log_for_create(product)
            id = await uow.card.add_one(data)
            await uow.commit()
            return id

    async def update_card(self, uow: IUnitOfWork, product: CardUpdate, admin_id: int):
        data = product.model_dump()
        async with uow:
            await ManualLogger(admin_id, uow).log_for_update(product.id, product)
            id = await uow.card.edit_one(product.id, data)
            await uow.commit()
            return id

    async def delete_card(self, uow: IUnitOfWork, id: int, admin_id: int):
        async with uow:
            await ManualLogger(admin_id, uow).log_for_delete(id)

            await uow.card.delete_one(id=id)
            await uow.commit()
