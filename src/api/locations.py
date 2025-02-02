from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.items import LocationCreate
from src.services.location_service import LocationService

router = APIRouter(
    tags=['location'],
    prefix='/locations',
)


@router.get('/get_locations')
async def get_locations(
        page: int,
        limit: int,
        uow: UOWDep
):
    location_service = LocationService()
    list_locations = await location_service.get_list_locations(uow, page, limit)
    return list_locations


@router.post('/add_location')
async def add_location(
        location: LocationCreate,
        uow: UOWDep
):
    location_service = LocationService()
    await location_service.add_location(uow,location)
    return {
        'status': 'ok',
    }
