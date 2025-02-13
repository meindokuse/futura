from datetime import date, datetime, timedelta

from sqlalchemy import select

from src.data.repository import SQLAlchemyRepository

from src.models.items import Events


class EventRepository(SQLAlchemyRepository):
    model = Events

    async def get_not_actually_events(self, page: int, limit: int, **filter_by):
        today = date.today()

        offset = (page - 1) * limit

        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .where(self.model.date_start < today)
            .order_by(self.model.date_start.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_events_actually(self, page: int, limit: int, **filter_by):
        today = date.today()

        offset = (page - 1) * limit

        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .where(self.model.date_start >= today)
            .order_by(self.model.date_start.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready

    async def get_latest_event(self,**filter_by):
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .order_by(self.model.date_start.desc())  # Сортируем по дате в убывающем порядке
            .limit(1)  # Берём только первую запись
        )
        result = await self.session.execute(stmt)
        return result.scalars().first().to_read_model()

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

        res_ready = [row[0].to_read_model() for row in result.all()]
        return res_ready
