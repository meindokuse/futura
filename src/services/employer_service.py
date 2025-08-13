from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException
from fastapi_mail import MessageSchema, FastMail

from src.data.unitofwork import IUnitOfWork
from src.schemas.peoples import EmployerCreate, EmployerUpdateAdmin
from src.smtp_config import mail_conf
from src.utils.jwt_tokens import bcrypt_context


class EmployerService:

    async def _send_email_registration(self, email: str, password: str):
        """
        Отправить email-уведомление о регистрации в системе HP Employers

        Args:
            email: Email адрес получателя (логин)
            password: Пароль для входа в систему
        """
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #2a52be;">Добро пожаловать в HP Employers!</h2>
            <p>Вы успешно зарегистрированы в системе.</p>

            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="margin-top: 0;">Ваши данные для входа:</h3>
                <p><strong>Логин (email):</strong> {email}</p>
                <p><strong>Пароль:</strong> {password}</p>
            </div>

            <p>Рекомендуем изменить пароль после первого входа в систему.</p>

            <p style="color: #666; font-size: 12px;">
                Это автоматическое сообщение, пожалуйста, не отвечайте на него.
                <br>Дата отправки: {datetime.now().strftime('%d.%m.%Y %H:%M')}
            </p>
        </body>
        </html>
        """

        message = MessageSchema(
            subject="✅ Регистрация в HP Employers",
            recipients=[email],
            body=html_content,
            subtype="html"
        )

        fm = FastMail(mail_conf)
        await fm.send_message(message)

    async def get_list_employers(
            self,
            fio: str,
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
                fio=fio,
            )
            return list_employers

    async def get_employers_by_work_type(self, work_type: str, uow: IUnitOfWork, fio: Optional[str] = None):
        async with uow:
            return await uow.employers.get_employer_by_work_type(work_type, fio)

    async def get_current_employer(self, uow: IUnitOfWork, id: int):
        async with uow:
            employer = await uow.employers.get_current_employer(id=id)
        return employer

    async def validate_email(self, email: str, uow: IUnitOfWork):
        async with uow:
            employer = await uow.employers.valid_employer(email=email)
            print(employer)
            if not employer:
                return False
            return True

    async def authenticate(self, uow: IUnitOfWork, email: str, password: str):
        async with uow:
            employer = await uow.employers.valid_employer(email=email)
            if not employer:
                return False
            if not bcrypt_context.verify(password, employer.hashed_password):
                return False
            return employer

    async def is_exist_email(self, uow: IUnitOfWork, email: str):
        async with uow:
            employer = await uow.employers.valid_employer(email=email)
            if not employer:
                return False
            else:
                return True

    async def get_list_of_birth(self, uow: IUnitOfWork, page: int, limit: int):
        async with uow:
            list_of_birth = await uow.employers.get_list_of_birth(page, limit)
            return list_of_birth

    # ДЛЯ АДМИНА
    async def add_employer(self, uow: IUnitOfWork, employer: EmployerCreate):
        async with uow:
            try:
                # Проверяем, существует ли уже работник с таким ФИО
                is_exist_fio = await uow.employers.valid_employer(fio=employer.fio)
                if is_exist_fio:
                    raise HTTPException(status_code=409, detail='Name already registered')

                # Проверяем, существует ли уже работник с таким email
                if_exist_email = await uow.employers.valid_employer(email=employer.email)
                if if_exist_email:
                    raise HTTPException(status_code=409, detail='Email already registered')
                print('начал хеш')

                # Хэшируем пароль
                hash_password = bcrypt_context.hash(employer.hashed_password)
                print('закончил хеш')

                # Преобразуем данные в формат, совместимый с моделью Employer
                data = {
                    "email": employer.email,
                    "fio": employer.fio.lower(),
                    "work_type": employer.work_type.lower(),
                    "roles": employer.roles,  # JSON автоматически сериализуется
                    "contacts": employer.contacts,  # JSON автоматически сериализуется
                    "description": employer.description,
                    "hashed_password": hash_password,
                    "date_of_birth": employer.date_of_birth,
                    "location_id": employer.location_id,
                }

                # Добавляем данные в таблицу employer
                id = await uow.employers.add_one(data)
                print('закончил добавление')

                await self._send_email_registration(employer.email, employer.hashed_password)
                await uow.commit()
                return id
            except Exception as e:
                await uow.rollback()
                print("Ошибка при регистрации", e)

    async def edit_employer(self, uow: IUnitOfWork, new_data: dict, id: int):
        async with uow:
            await uow.employers.edit_one(id=id, data=new_data)
            await uow.commit()

    async def edit_email(self, uow: IUnitOfWork, email: str, user_id: int):
        async with uow:
            id = await uow.employers.edit_one(id=user_id, data={"email": email})
            await uow.commit()
            return id

    async def edit_password(self, uow: IUnitOfWork, old_password: str, new_password: str, user_id: int):
        async with uow:
            employer = await uow.employers.valid_employer(id=user_id)
            if not employer:
                return False
            if not bcrypt_context.verify(old_password, employer.hashed_password):
                return False
            hash_password = bcrypt_context.hash(new_password)
            await uow.employers.edit_one(id=user_id, data={'hashed_password': hash_password})
            await uow.commit()
            return True

    async def edit_password_after_validate(self, uow: IUnitOfWork, new_password: str, email: str):
        async with uow:
            hash_password = bcrypt_context.hash(new_password)
            await uow.employers.change_password_by_email(email=email, password=hash_password)
            await uow.commit()
            return True

    async def delete_employer(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.employers.delete_one(id=id)
            await uow.commit()
