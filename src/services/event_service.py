import datetime

from src.data.unitofwork import IUnitOfWork
from src.logs.loggers.event_logger import EventLogger
from src.schemas.items import EventCreate, EventFilter, EventUpdate
from src.schemas.logs import LogsCreate
from src.utils.log_decorator import log_action
from src.utils.log_enum import LogType, LogAction


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

    async def get_events_filters(self, uow: IUnitOfWork, filters: EventFilter, date_filter: datetime.date):
        async with uow:
            list_events = await uow.event.get_event_with_filters(filters=filters, date_filter=date_filter)
            return list_events

    async def get_latest_event(self, uow: IUnitOfWork):
        async with uow:
            event = await uow.event.get_latest_event()
            return event

    async def add_event(self, uow: IUnitOfWork, event: EventCreate, admin_id: int):
        data = event.model_dump()
        async with uow:
            await EventLogger(admin_id, uow).log_for_create(event)
            id = await uow.event.add_one(data)
            await uow.commit()
            return id

    async def delete_event(self, uow: IUnitOfWork, id: int, admin_id: int):
        async with uow:
            await EventLogger(admin_id, uow).log_for_delete(id)
            await uow.event.delete_one(id=id)
            await uow.commit()

    async def update_event(self, uow: IUnitOfWork, id: int, event: EventUpdate,admin_id: int):
        data = event.model_dump()
        async with uow:
            await EventLogger(admin_id, uow).log_for_update(id,event)
            await uow.event.update_event(data, id)
            await uow.commit()
