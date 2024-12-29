from abc import ABC, abstractmethod
from typing import Type

from src.db.database import async_session_maker
from src.repositories.items.event_repository import EventRepository
from src.repositories.items.product_repository import ProductRepository
from src.repositories.peoples.employer_repository import EmployerRepository
from src.repositories.peoples.residents_repository import ResidentsRepository
from src.repositories.items.work_repository import WorkRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    residents: Type[ResidentsRepository]
    employers: Type[EmployerRepository]

    work_day: Type[WorkRepository]
    product: Type[ProductRepository]
    event: Type[EventRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.residents = ResidentsRepository(self.session)
        self.employers = EmployerRepository(self.session)
        self.work_day = WorkRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
