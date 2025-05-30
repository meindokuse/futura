from typing import Optional

from fastapi import APIRouter
from src.api.dependses import UOWDep
from datetime import date

from src.schemas.items import EventCreate, EventFilter, EventsUpdate
from src.services.event_service import EventService
from src.utils.message_manager import MessageManager
import asyncio

router = APIRouter(
    tags=['events'],
    prefix='/events',
)


# @router.get('/get_not_actually_events')
# async def get_not_actually_events(
#         uow: UOWDep,
#         page: int,
#         limit: int,
#         location_id: Optional[int] = None,
# ):
#     events_service = EventService()
#     events = await events_service.get_not_actually_events(uow, page, limit, location_id)
#     return events
#
#
# @router.get("/get_events")
# async def get_events(
#         uow: UOWDep,
#         page: int,
#         limit: int,
#         location_id: Optional[int] = None,
# ):
#     events_service = EventService()
#     events = await events_service.get_event_list(uow, page, limit, location_id)
#     return events
#
#
# @router.get('/get_events_by_date')
# async def get_events_by_date(
#         uow: UOWDep,
#         page: int,
#         limit: int,
#         target_date: date,
#         location_id: Optional[int] = None,
# ):
#     events_service = EventService()
#     events = await events_service.get_event_list_by_date(uow, page, limit, target_date, location_id)
#     return events

@router.get('/get_events_with_filters')
async def get_events_with_filters(
        uow: UOWDep,
        page: int,
        limit: int,
        target_date: Optional[date] = None,
        name: Optional[str] = None,
        location_id: Optional[int] = None,
):
    events_service = EventService()
    filters = EventFilter(
        page=page,
        limit=limit,
        location_id=location_id,
        name=name,
    )
    events = await events_service.get_events_filters(uow, filters, target_date)
    return events


@router.get('/get_latest')
async def get_latest(
        uow: UOWDep,
):
    events_service = EventService()
    event = await events_service.get_latest_event(uow)
    return event


@router.post("/admin/create_event")
async def create_event(
        event: EventCreate,
        uow: UOWDep
):
    events_service = EventService()
    id = await events_service.add_event(uow, event)
    if id:
        start = event.date_start.strftime("%d/%m/%Y, %H:%M")
        text = f'Анонсировано новое событие!\n{event.name}\nНачало: {start}\nПолная информация на нашем сайте.'
        print(f"Текст для отправки: {text}")
        asyncio.create_task(MessageManager.send_message_to_bot(text=text))

    return {
        "status": "success",
    }


@router.delete("/admin/delete_event")
async def delete_event(
        id: int,
        uow: UOWDep
):
    events_service = EventService()
    await events_service.delete_event(uow, id)
    return {
        "status": "success",
    }


@router.put("/admin/update_event")
async def update_event(
        id: int,
        event: EventsUpdate,
        uow: UOWDep
):
    events_service = EventService()
    await events_service.update_event(uow, id, event)
    return {
        "status": "success",
    }
