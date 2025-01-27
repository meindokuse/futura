import datetime

from src.data.unitofwork import IUnitOfWork
from src.schemas.items import EventRead, EventCreate


class EventService:

    async def get_event_list(self, uow: IUnitOfWork, page: int, limit: int, date: datetime.date):
        async with uow:
            list_events = await uow.event.find_all(page=page, limit=limit, date=date)
            return list_events

    async def add_event(self, uow: IUnitOfWork, event: EventCreate):
        async with uow:
            await uow.event.add_one(event)

    async def delete_event(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.event.delete_one(id=id)
