from abc import ABC, abstractmethod

from src.data.unitofwork import IUnitOfWork, UnitOfWork


class ILogger(ABC):
    def __init__(self, admin_id: int, uow: IUnitOfWork):
        self.admin_id = admin_id
        self.uow = uow

    @abstractmethod
    async def log_for_create(self, data):
        pass

    @abstractmethod
    async def log_for_delete(self, id: int):
        pass

    @abstractmethod
    async def log_for_update(self, id: int, data):
        pass
