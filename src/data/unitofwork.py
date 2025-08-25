from abc import ABC, abstractmethod
from typing import Type

from src.db.database import async_session_maker
from src.repositories.items.event_repository import EventRepository
from src.repositories.items.location_repository import LocationRepository
from src.repositories.items.card_repository import CardRepository
from src.repositories.items.logs_repository import LogsRepository
from src.repositories.peoples.employer_repository import EmployerRepository
from src.repositories.peoples.residents_repository import ResidentsRepository
from src.repositories.items.work_repository import WorkRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    residents: ResidentsRepository
    employers: EmployerRepository

    work_day: WorkRepository
    card: CardRepository
    event: EventRepository
    location: LocationRepository
    logs: LogsRepository

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


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.residents = ResidentsRepository(self.session)
        self.employers = EmployerRepository(self.session)
        self.work_day = WorkRepository(self.session)
        self.card = CardRepository(self.session)
        self.event = EventRepository(self.session)
        self.location = LocationRepository(self.session)
        self.logs = LogsRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        print('commit')
        await self.session.commit()

    async def rollback(self):
        print('rollback')

        await self.session.rollback()
