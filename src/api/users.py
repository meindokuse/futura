from datetime import timedelta
from typing import Annotated

from authx import AuthXConfig, AuthX
from fastapi import APIRouter, Response, HTTPException, Depends

from src.api.dependses import UOWDep
from src.schemas.peoples import EmployerCreate, EmployerRead
from src.services.EmployerService import EmployerService
from src.utils.jwt_tokens import create_access_token, get_current_user, user_dep

router = APIRouter(
    tags=['auth'],
    prefix='/auth',
)


@router.get('/login')
async def login_for_get_token(email: str, password: str, response: Response, uow: UOWDep):
    user = await EmployerService().authenticate(uow, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(user.fio, timedelta(minutes=60))

    return {"message": "Login successful", "access_token": token}


@router.get('/enter')
async def enter_and_get_profile(user: user_dep, uow: UOWDep):
    user = await EmployerService().get_current_employer(uow, user.get('fio'))
    return user


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
