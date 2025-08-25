from typing import Optional

from fastapi import APIRouter, Query

from src.api.dependses import UOWDep
from src.models.items import LogType, LogAction
from src.schemas.items import CardCreate, CardUpdate
from src.schemas.logs import LogsCreate
from src.schemas.other_requests import DeleteRequest
from src.services.card_service import CardService
from src.utils.jwt_tokens import user_dep

router = APIRouter(
    tags=['cards'],
    prefix='/cards',
)


@router.post('/admin/add_card')
async def add_card(uow: UOWDep, card: CardCreate, user: user_dep):
    card_service = CardService()
    id = await card_service.add_card(uow, card, int(user.id))

    return {
        "status": "success",
        'id': id
    }


@router.put('/admin/update_manual')
async def add_card(uow: UOWDep, card: CardUpdate, user: user_dep):
    card_service = CardService()
    id = await card_service.update_card(uow, card, int(user.id))

    return {
        "status": "success",
        'id': id
    }


@router.get('/get_list_cards')
async def get_list_cards(uow: UOWDep, page: int, limit: int,
                         title: Optional[str] = None, location_id: Optional[int] = None):
    print(location_id, "Локация для фильтрации")
    card_service = CardService()

    list_cards = await card_service.get_list_cards(uow=uow, page=page, limit=limit, title=title,
                                                   location_id=location_id)
    return list_cards


@router.delete('/admin/delete_card')
async def delete_product(uow: UOWDep, id: int, user: user_dep):
    card_service = CardService()
    await card_service.delete_card(uow=uow, id=id, admin_id=int(user.id))
    return {
        "status": "success",
    }
