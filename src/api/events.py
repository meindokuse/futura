from datetime import datetime

from fastapi import APIRouter
from src.api.dependses import UOWDep
from datetime import date

from src.schemas.items import EventCreate
from src.services.event_service import EventService
from src.utils.notify import send_message_to_bot
import asyncio

router = APIRouter(
    tags=['events'],
    prefix='/events',
)


@router.get('/get_not_actually_events')
async def get_not_actually_events(
        page: int,
        limit: int,
        uow: UOWDep
):
    events_service = EventService()
    events = await events_service.get_not_actually_events(uow, page, limit)
    return events


@router.get("/get_events")
async def get_events(
        page: int,
        limit: int,
        uow: UOWDep
):
    events_service = EventService()
    events = await events_service.get_event_list(uow, page, limit)
    return events


@router.get('/get_events_by_date')
async def get_events_by_date(
        page: int,
        limit: int,
        target_date: date,
        uow: UOWDep
):
    events_service = EventService()
    events = await events_service.get_event_list_by_date(uow, page, limit, target_date)
    return events
@router.get('/get_latest')
async def get_latest(uow:UOWDep):
    events_service = EventService()
    event = await events_service.get_latest_event(uow)
    return event

@router.post("/create_event")
async def create_event(
        event: EventCreate,
        uow: UOWDep
):
    events_service = EventService()
    id = await events_service.add_event(uow, event)
    if id:
        start = event.date_start.strftime("%d/%m/%Y, %H:%M")
        text = f'Анонсировано новое событие!\n{event.name}\nНачало: {start}\nПолная информация на нашем сайте.'
        asyncio.create_task(send_message_to_bot(text))

    return {
        "status": "success",
    }


@router.delete("/delete_event")
async def delete_event(
        id: int,
        uow: UOWDep
):
    events_service = EventService()
    await events_service.delete_event(uow, id)
    return {
        "status": "success",
    }
