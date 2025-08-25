from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import select, func, and_, update, delete
from sqlalchemy.orm import selectinload, joinedload

from src.data.repository import SQLAlchemyRepository

from src.models.items import Events, Location
from src.schemas.items import EventFilter


class EventRepository(SQLAlchemyRepository):
    model = Events

    async def get_latest_event(self, **filter_by):
        stmt = (
            select(Events)
            .options(
                selectinload(Events.location),  # Загружаем связанный Location
            )
            .filter_by(**filter_by)  # Фильтруем по атрибутам Events
            .order_by(Events.date_start.desc())  # Сортируем по дате в убывающем порядке
            .limit(1)  # Берём только первую запись
        )

        result = await self.session.execute(stmt)
        event = result.scalars().first()
        return event.to_read_model() if event else None

    async def get_events_by_date(self, target_date: date, page: int, limit: int, **filter_by):
        offset = (page - 1) * limit

        # Создаем диапазон дат для фильтрации
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)

        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .where(self.model.date_start >= start_datetime, self.model.date_start < end_datetime)
            .order_by(self.model.date_start.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        res_ready = [row[0].to_read_model_second() for row in result.all()]
        return res_ready

    async def get_event_with_filters(self, filters: EventFilter, date_filter: Optional[date] = None):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.location))
            .order_by(self.model.date_start.desc())
        )

        conditions = []

        # Фильтр по дате
        if date_filter and isinstance(date_filter, date):
            conditions.append(func.date(self.model.date_start) == date_filter)
        else:
            # Если дата не задана, показываем только актуальные события (начиная с сегодня)
            conditions.append(func.date(self.model.date_start) >= date.today())

        # Фильтр по названию события
        if filters.name:
            conditions.append(self.model.name.ilike(f"%{filters.name}%"))

        # Фильтр по location_id (включая None)
        if hasattr(filters, 'location_id'):
            if filters.location_id is not None:
                conditions.append(self.model.location_id == filters.location_id)
            else:
                conditions.append(self.model.location_id.is_(None))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.offset((filters.page - 1) * filters.limit).limit(filters.limit)

        result = await self.session.execute(stmt)
        events = result.scalars().all()
        return [ev.to_read_model() for ev in events] if events else []

    async def update_event(self, data: dict, id: int):
        stmt = update(self.model).values(data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_event_for_logs(self, id: int):
        stmt = (
            select(Events)
            .where(self.model.id == id)
            .limit(1)  # Берём только первую запись
        )

        result = await self.session.execute(stmt)
        event = result.scalars().first()
        return event.read_for_logs() if event else None


