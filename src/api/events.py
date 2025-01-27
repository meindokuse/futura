from datetime import datetime

from fastapi import APIRouter
from src.api.dependses import UOWDep
from datetime import date

from src.schemas.items import EventCreate
from src.services.event_service import EventService

router = APIRouter(
    tags=['events'],
    prefix='/events',
)


@router.get("/get_events")
async def get_events(
        page: int,
        limit: int,
        target_date: date,
        uow: UOWDep
):
    events_service = EventService()
    events = await events_service.get_event_list(uow, page, limit, target_date)
    return events

@router.post("/create_event")
async def create_event(
        event: EventCreate,
        uow: UOWDep
):
    events_service = EventService()
    await events_service.add_event(uow,event)
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
