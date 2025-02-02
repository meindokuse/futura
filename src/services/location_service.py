from src.data.unitofwork import IUnitOfWork
from src.models.items import Location
from src.schemas.items import LocationCreate


class LocationService:
    async def get_list_locations(self, uow: IUnitOfWork, page: int, limit: int):
        async with uow:
            list_locations = await uow.location.find_all(page=page, limit=limit)
            return list_locations

    async def add_location(self, uow: IUnitOfWork, location: LocationCreate):
        data = location.model_dump()
        async with uow:
            await uow.location.add_one(data=data)
            await uow.commit()
