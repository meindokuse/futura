from typing import Optional

from fastapi import HTTPException

from src.data.unitofwork import IUnitOfWork
from src.schemas.peoples import EmployerCreate, EmployerRead
from src.utils.jwt_tokens import bcrypt_context


class EmployerService:

    async def get_list_employers(
            self,
            uow: IUnitOfWork,
            page: int,
            limit: int,
            sort_by: str = "fio",
            sort_order: str = "asc",
            filter_by: Optional[dict] = None,
    ):
        async with uow:
            list_employers = await uow.employers.get_employees(
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
                filter_by=filter_by or {},
            )
            return list_employers
    async def get_current_employer(self, uow: IUnitOfWork, id: int):
        async with uow:
            employer = await uow.employers.find_one(id=id)
        return employer

    async def authenticate(self, uow: IUnitOfWork, email: str, password: str):
        async with uow:
            employer = await uow.employers.find_one(email=email)
            if not employer:
                return False
            if not bcrypt_context.verify(password, employer.password):
                return False
            return employer

    # ДЛЯ АДМИНА
    async def add_employer(self, uow: IUnitOfWork, employer: EmployerCreate):
        async with uow:
            # Проверяем, существует ли уже работник с таким ФИО
            is_exist_fio = await uow.employers.find_one(fio=employer.fio)
            if is_exist_fio:
                raise HTTPException(status_code=401, detail='Name already registered')

            # Проверяем, существует ли уже работник с таким email
            if_exist_email = await uow.employers.find_one(email=employer.email)
            if if_exist_email:
                raise HTTPException(status_code=401, detail='Email already registered')

            # Хэшируем пароль
            hash_password = bcrypt_context.hash(employer.hashed_password)

            # Преобразуем данные в формат, совместимый с моделью Employer
            data = {
                "email": employer.email,
                "fio": employer.fio,
                "work_type": employer.work_type,
                "roles": employer.roles,  # JSON автоматически сериализуется
                "image": employer.image,
                "contacts": employer.contacts,  # JSON автоматически сериализуется
                "description": employer.description,
                "hashed_password": hash_password,
            }

            # Добавляем данные в таблицу employer
            await uow.employers.add_one(data)
            await uow.commit()

    async def edit_employer(self, uow: IUnitOfWork, new_data: EmployerRead, id: int):
        new_data_dict = new_data.model_dump()
        async with uow:
            await uow.employers.edit_one(id=id, data=new_data_dict)

    async def delete_employer(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.employers.delete_one(id=id)
            await uow.commit()
