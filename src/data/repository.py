from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, page: int, limit: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_table(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, page: int, limit: int, **filter_by):
        if limit == 0:

            stmt = (select(self.model)
                    .filter_by(**filter_by))

            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

        else:
            start = (page - 1) * limit

            stmt = (select(self.model)
                    .filter_by(**filter_by)
                    .order_by(self.model.id)
                    .offset(start)
                    .limit(limit))
            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res


    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            return res.to_read_model()
        return None
    async def delete_one(self,**filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
