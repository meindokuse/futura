from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.peoples import ResidentCreate
from src.services.residents_service import ResidentsService

router = APIRouter(
    tags=['residents'],
    prefix='/residents',
)


@router.get('/get_list_residents')
async def get_list_residents(page: int, limit: int, uow: UOWDep):
    list_residents = await ResidentsService().get_list_residents(uow, page, limit)
    return list_residents

@router.get('/get_resident')
async def get_resident(fio: str, uow: UOWDep):
    resident = await ResidentsService().get_current_resident(uow,fio)
    return resident


@router.post('/add_resident')
async def add_new_resident(resident: ResidentCreate, uow: UOWDep):
    await ResidentsService().add_resident(uow, resident)
    return {
        "status": "ok",
    }


@router.delete('/delete_resident')
async def delete_resident(fio: str, uow: UOWDep):
    await ResidentsService().delete_resident(uow, fio)
    return {
        "status": "ok",
    }
