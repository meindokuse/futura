from typing import Optional

from fastapi import APIRouter

from src.api.dependses import UOWDep
from src.schemas.peoples import EmployerCreate, EmployerRead, EmployerUpdateAdmin, EmployerUpdateBasic
from src.services.employer_service import EmployerService
from src.utils.jwt_tokens import user_dep

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


@router.get('/get_employer_by_work_type')
async def get_employer_by_work_type(uow: UOWDep, work_type: str, fio: Optional[str] = None):
    employer_service = EmployerService()
    employers = await employer_service.get_employers_by_work_type(work_type.lower(), uow, fio)
    return employers


@router.get("/get_employer")
async def get_employer(uow: UOWDep, id: int):
    employer_service = EmployerService()
    employer = await employer_service.get_current_employer(uow, id)
    return employer


@router.put('/edit_employer')
async def edit_employer(uow: UOWDep, user: user_dep, new_data: EmployerUpdateBasic):
    new_data_dict = new_data.model_dump()
    await EmployerService().edit_employer(uow, new_data_dict, int(user.id))
    return {
        "status": "ok"
    }


@router.put('/admin/edit_employer')
async def edit_employer(employer_id: int, new_data: EmployerUpdateAdmin, uow: UOWDep):
    new_data_dict = new_data.model_dump()
    await EmployerService().edit_employer(uow, new_data_dict, employer_id)
    return {
        "status": "ok"
    }


@router.put('/admin/edit_password')
async def edit_employer(employer_id: int, password: str, uow: UOWDep):
    await EmployerService().edit_password(uow, password, employer_id)
    return {
        "status": "ok"
    }


@router.get('/get_list_birth')
async def get_list_birth(uow: UOWDep, page: int, limit: int):
    list_birth = await EmployerService().get_list_of_birth(uow, page, limit)
    return list_birth


@router.delete('/admin/delete_employer')
async def delete_employer(employer_id: int, uow: UOWDep):
    await EmployerService().delete_employer(uow, employer_id)
    return {
        "status": "ok"
    }
