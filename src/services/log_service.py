from src.data.unitofwork import IUnitOfWork
from src.schemas.logs import LogsFilters


class LogService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_logs(self, filters: LogsFilters):
        async with self.uow:
            return await self.uow.logs.get_logs(filters)
