from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.items import Logs, WorkDay
from src.models.peoples import Employer
from src.schemas.logs import LogsFilters
from src.utils.log_enum import LogType


class LogsRepository(SQLAlchemyRepository):
    model = Logs

    async def get_logs(self, filters: LogsFilters):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.location),
                selectinload(self.model.employer),
            )
        )
        if filters.type:
            stmt = stmt.where(self.model.type == filters.type)
        if filters.action:
            stmt = stmt.where(self.model.action == filters.action)
        if filters.date_created:
            stmt = stmt.where(self.model.date_created == filters.date_created)

        stmt = stmt.where(self.model.location_id == filters.location_id)


        stmt = stmt.order_by(self.model.date_created.desc(), self.model.time_created.desc())
        stmt.offset(filters.page).limit(filters.limit)
        result = await self.session.execute(stmt)
        return [log.to_read_model() for log in result.scalars().all()]




