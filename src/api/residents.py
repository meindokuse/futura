from typing import Optional

from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.peoples import ResidentCreate, ResidentUpdate
from src.services.residents_service import ResidentsService

router = APIRouter(
    tags=['residents'],
    prefix='/residents',
)


@router.get('/get_list_residents')
async def get_list_residents(page: int, limit: int, uow: UOWDep):
    list_residents = await ResidentsService().get_list_residents(uow, page, limit)
    return list_residents


@router.get('/get_residents_by_filters')
async def get_residents_by_filters(uow: UOWDep,page: int, limit: int, fio: Optional[str] = None):
    residents = await ResidentsService().get_residents_with_filter(uow, fio, page, limit)
    return residents


@router.get('/get_resident')
async def get_resident(id: int, uow: UOWDep):
    resident = await ResidentsService().get_current_resident(uow, id)
    return resident


@router.post('/add_resident')
async def add_new_resident(resident: ResidentCreate, uow: UOWDep):
    id = await ResidentsService().add_resident(uow, resident)
    return {
        "status": "ok",
        'id':id
    }


@router.delete('/delete_resident')
async def delete_resident(id: int, uow: UOWDep):
    await ResidentsService().delete_resident(uow, id)
    return {
        "status": "ok",
    }

@router.put('/update_resident')
async def update_resident(id:int,resident: ResidentUpdate, uow: UOWDep):
    await ResidentsService().update_resident(uow,resident,id)
    return {
        "status": "ok",
    }

