

from fastapi import HTTPException

from src.data.unitofwork import IUnitOfWork
from src.schemas.peoples import EmployerCreate
from src.utils.jwt_tokens import bcrypt_context


class EmployerService:
    async def get_list_employer(self, uow: IUnitOfWork, page: int, limit: int):
        async with uow:
            list_residents = await uow.residents.find_all(page=page, limit=limit)
            return list_residents

    async def get_current_employer(self, uow: IUnitOfWork, fio: str):
        async with uow:
            employer = await uow.employers.find_one(fio=fio)
        return employer

    async def authenticate(self, uow: IUnitOfWork, email: str, password: str):
        async with uow:
            employer = await uow.employers.find_one(email=email)
            if not employer:
                return False
            if not bcrypt_context.verify(password, employer.password):
                return False
            return employer

    # async def get_list_work_days_for_current_employer(self, uow: IUnitOfWork, fio: Optional[str] = None):
    #     async with uow:
    #         if fio is None:
    #             employer = await uow.employers.find_one(id=id)
    #         else:
    #             employer = await get_current_user(uow)
    #
    #         return employer.work_days

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
                "is_active": employer.is_active,
                "image": employer.image,
                "contacts": employer.contacts,  # JSON автоматически сериализуется
                "description": employer.description,
                "hashed_password": hash_password,
            }

            # Добавляем данные в таблицу employer
            await uow.employers.add_one(data)
            await uow.commit()




