from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.peoples import ResidentCreate
from src.services.residents_service import ResidentsService

router = APIRouter(
    tags=['residents'],
    prefix='/residents',
)


@router.get('/{location_name}/get_list_residents')
async def get_list_residents(page: int, limit: int, uow: UOWDep):
    list_residents = await ResidentsService().get_list_residents(uow, page, limit)
    return list_residents


@router.get('/{location_name}/get_resident_by_fio')
async def get_resident(page: int, limit: int, fio: str, uow: UOWDep):
    residents = await ResidentsService().get_current_residents(uow, fio, page, limit)
    return residents


@router.post('/add_resident')
async def add_new_resident(resident: ResidentCreate, uow: UOWDep):
    await ResidentsService().add_resident(uow, resident)
    return {
        "status": "ok",
    }


@router.delete('/delete_resident')
async def delete_resident(id: int, uow: UOWDep):
    await ResidentsService().delete_resident(uow, id)
    return {
        "status": "ok",
    }
