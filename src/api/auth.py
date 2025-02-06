from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependses import UOWDep
from src.schemas.peoples import EmployerCreate
from src.services.EmployerService import EmployerService
from src.services.work_service import WorkService
from src.utils.jwt_tokens import create_access_token, user_dep, Token

router = APIRouter(
    tags=['auth'],
    prefix='/auth',
)


@router.post('/token')
async def login_for_get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], uow: UOWDep):
    try:
        user = await EmployerService().authenticate(uow, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        token = create_access_token(user.id, user.roles, user.fio, timedelta(minutes=60))

        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/profile')
async def get_profile(user: user_dep, uow: UOWDep):
    user_data = await EmployerService().get_current_employer(uow, int(user.get('id')))
    work_days = await WorkService().get_list_workdays_for_current_employer(uow, user.get('fio'), 1, 10)
    return {
        "user": user_data,
        "work_days": work_days
    }


@router.post('/admin/register')
async def register(new_user: EmployerCreate, uow: UOWDep):
    await EmployerService().add_employer(uow, new_user)
    return {
        'status': 'success',
    }

# @router.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
#     return {"message": "Logged out successfully"}
