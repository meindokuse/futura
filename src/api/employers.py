from typing import Optional

from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.peoples import EmployerCreate, EmployerRead, EmployerUpdate
from src.services.EmployerService import EmployerService

router = APIRouter(
    tags=['employers'],
    prefix='/employers',
)


@router.get("/get_list_employers/{location_id}")
async def list_employers(
        uow: UOWDep,
        location_id: int,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "fio",
        sort_order: str = "asc",
        work_type: Optional[str] = None,
        fio: Optional[str] = None,

):
    filter_by = {"location_id": location_id}

    if work_type:
        filter_by["work_type"] = work_type.lower()

    employer_service = EmployerService()
    employers = await employer_service.get_list_employers(
        uow=uow,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        filter_by=filter_by,
        fio=fio
    )
    return employers


@router.get("/get_employer")
async def get_employer(uow: UOWDep, id: int):
    employer_service = EmployerService()
    employer = await employer_service.get_current_employer(uow, id)
    return employer


@router.put('/edit_employer')
async def edit_employer(employer_id: int, new_data: EmployerUpdate, uow: UOWDep):
    await EmployerService().edit_employer(uow, new_data, employer_id)
    return {
        "status": "ok"
    }


@router.get('/get_list_birth')
async def get_list_birth(uow: UOWDep, page: int, limit: int):
    list_birth = await EmployerService().get_list_of_birth(uow, page, limit)
    return list_birth


@router.delete('/delete_employer')
async def delete_employer(employer_id: int, uow: UOWDep):
    await EmployerService().delete_employer(uow, employer_id)
    return {
        "status": "ok"
    }
