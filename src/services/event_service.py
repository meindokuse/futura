import datetime

from src.data.unitofwork import IUnitOfWork
from src.schemas.items import EventCreate


class EventService:

    async def get_not_actually_events(self, uow: IUnitOfWork, page: int, limit: int, location_id: int):
        async with uow:
            list_events = await uow.event.get_not_actually_events(page=page, limit=limit, location_id=location_id)
            return list_events

    async def get_event_list(self, uow: IUnitOfWork, page: int, limit: int, location_id: int):
        async with uow:
            list_events = await uow.event.get_events_actually(page=page, limit=limit, location_id=location_id)
            return list_events

    async def get_event_list_by_date(self, uow: IUnitOfWork, page: int, limit: int, date: datetime.date,
                                     location_id: int):
        async with uow:
            list_events = await uow.event.get_events_by_date(page=page, limit=limit, target_date=date,
                                                             location_id=location_id)
            return list_events

    async def get_latest_event(self, uow: IUnitOfWork):
        async with uow:
            event = await uow.event.get_latest_event()
            return event

    async def add_event(self, uow: IUnitOfWork, event: EventCreate):
        data = event.model_dump()
        async with uow:
            id = await uow.event.add_one(data)
            await uow.commit()
            return id

    async def delete_event(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.event.delete_one(id=id)
            await uow.commit()
