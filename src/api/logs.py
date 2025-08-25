from fastapi import APIRouter, HTTPException

from src.api.dependses import UOWDep
from src.schemas.logs import LogsFilters
from src.services.log_service import LogService
from src.utils.log_enum import LogType, LogAction

router = APIRouter(
    tags=['logs'],
    prefix='/logs',
)


@router.post('/admin/get_list')
async def get_list_logs(
        uow: UOWDep,
        filters: LogsFilters
):
    # if filters.type:
    #     try:
    #         print(filters.type)
    #         filters.type = LogType(filters.type)
    #     except ValueError:
    #         raise HTTPException(status_code=422, detail="Invalid type value")
    #
    # if filters.action:
    #     try:
    #         filters.action = LogAction(filters.action)
    #     except ValueError:
    #         raise HTTPException(status_code=422, detail="Invalid action value")
    res = await LogService(uow).get_logs(filters)
    print(res)
    return res
