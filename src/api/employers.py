from typing import Optional

from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.peoples import EmployerCreate, EmployerRead, EmployerPut
from src.services.EmployerService import EmployerService

router = APIRouter(
    tags=['employers'],
    prefix='/employers',
)


@router.get("/get_list_employers")
async def list_employers(
        uow: UOWDep,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "fio",
        sort_order: str = "asc",
        location_id: Optional[int] = None,
        work_type: Optional[str] = None
):
    filter_by = {}

    if location_id:
        filter_by["location_id"] = location_id
    if work_type:
        filter_by["work_type"] = work_type

    employer_service = EmployerService()
    employers = await employer_service.get_list_employers(
        uow=uow,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        filter_by=filter_by,
    )
    return employers


@router.get("/get_employer")
async def get_employer(uow: UOWDep, id: int):
    employer_service = EmployerService()
    employer = await employer_service.get_current_employer(uow, id)
    return employer


@router.put('/edit_employer')
async def edit_employer(employer_id: int, new_data: EmployerPut, uow: UOWDep):
    await EmployerService().edit_employer(uow, new_data, employer_id)
    return {
        "status": "ok"
    }


@router.delete('/delete_employer')
async def delete_employer(employer_id: int, uow: UOWDep):
    await EmployerService().delete_employer(uow, employer_id)
    return {
        "status": "ok"
    }
