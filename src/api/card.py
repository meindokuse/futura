from typing import Optional

from fastapi import APIRouter, Query

from src.api.dependses import UOWDep
from src.schemas.items import CardCreate
from src.services.card_service import CardService

router = APIRouter(
    tags=['cards'],
    prefix='/cards',
)


@router.post('/admin/add_card')
async def add_card(uow: UOWDep, card: CardCreate):
    card_service = CardService()
    id = await card_service.add_card(uow, card)
    return {
        "status": "success",
        'id':id
    }


@router.get('/get_list_cards/')
async def get_list_cards(uow: UOWDep, page: int, limit: int,
                            type_product: Optional[str] = None, location_id: Optional[int] = None):
    card_service = CardService()

    list_cards = await card_service.get_list_cards(uow=uow, page=page, limit=limit, category=type_product,
                                                         location_id=location_id)
    return list_cards


@router.delete('/admin/delete_product')
async def delete_product(uow: UOWDep, id: int):
    card_service = CardService()
    await card_service.delete_card(uow=uow, id=id)
    return {
        "status": "success",
    }

