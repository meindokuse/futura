from operator import or_
from typing import Optional

from sqlalchemy import case
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Employer

from datetime import date, timedelta
from sqlalchemy import select, and_, or_, extract
from sqlalchemy.sql import func


class EmployerRepository(SQLAlchemyRepository):
    model = Employer

    async def valid_employer(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            return res.to_read_model_for_validate()
        return None

    async def get_employees(
            self,
            page: int,
            limit: int,
            sort_by: str = "fio",
            sort_order: str = "asc",
            filter_by: dict = None,
            fio: str = None,
    ):
        filter_by = filter_by or {}

        # Проверка, что переданный атрибут для сортировки существует
        if not hasattr(self.model, sort_by):
            raise AttributeError(f"Model Employer has no attribute '{sort_by}'.")

        # Определение порядка сортировки
        order_by = (
            getattr(self.model, sort_by).desc()
            if sort_order.lower() == "desc"
            else getattr(self.model, sort_by).asc()
        )

        # Пагинация
        start = (page - 1) * limit

        # Фильтрация по filter_by
        filters = [
            getattr(self.model, key) == value
            for key, value in filter_by.items()
            if hasattr(self.model, key)
        ]

        # Фильтрация по ФИО (если параметр передан)
        if fio:
            # Убираем пробелы в начале и конце, приводим к нижнему регистру
            fio_cleaned = fio.strip().lower()

            # Ищем частичное совпадение в поле ФИО
            filters.append(
                func.lower(func.trim(Employer.fio)).contains(fio_cleaned)
            )

        # Формируем запрос
        stmt = (
            select(self.model)
            .where(and_(*filters))  # Применяем все фильтры
            .order_by(order_by)  # Сортировка
            .offset(start)  # Пагинация
            .limit(limit)
        )

        # Выполняем запрос
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model_for_cards() for row in res.all()]
        return res

    async def get_current_employer(self, id: int):
        stmt = (
            select(Employer)
            .options(
                selectinload(Employer.location)
            )
            .where(Employer.id == id)
        )

        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res.to_read_model()

    async def get_employer_by_work_type(self, work_type: str, fio: Optional[str] = None):
        stmt = select(Employer)
        if work_type == 'хостес':
            stmt = stmt.where(or_(
                Employer.work_type == 'менеджер',
                Employer.work_type == 'хостес'
            ))
        if work_type == 'бармен':
            stmt = stmt.where(or_(
                Employer.work_type == 'бармен',
                Employer.work_type == 'помощник бармена'
            ))
        if work_type == 'кальянный мастер':
            stmt = stmt.where(or_(
                Employer.work_type == 'кальянный мастер',
                Employer.work_type == 'помощник кальянного мастера'
            ))

        if fio is not None:
            stmt = stmt.where(Employer.fio.ilike(f"%{fio}%"))
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model_for_cards() for row in res.all()]
        return res

    async def get_list_of_birth(self, page: int, limit: int):
        start = (page - 1) * limit
        today = date.today()

        # Определяем диапазон дней и месяцев для ближайших 3 дней
        day_month_pairs = [
            ((today + timedelta(days=i)).month, (today + timedelta(days=i)).day)
            for i in range(3)
        ]

        # Создаем условие для фильтрации
        conditions = []
        for month, day in day_month_pairs:
            conditions.append(
                and_(
                    extract('month', Employer.date_of_birth) == month,
                    extract('day', Employer.date_of_birth) == day,
                )
            )

        # Если диапазон переходит через год, добавляем условия для следующего года
        if (today + timedelta(days=3)).year != today.year:
            next_year_pairs = [
                ((today + timedelta(days=i)).replace(year=today.year + 1).month,
                 (today + timedelta(days=i)).replace(year=today.year + 1).day)
                for i in range(3)
            ]
            for month, day in next_year_pairs:
                conditions.append(
                    and_(
                        extract('month', Employer.date_of_birth) == month,
                        extract('day', Employer.date_of_birth) == day,
                    )
                )

        # Создаем выражение для сортировки по ближайшим дням рождения
        order_by_case = case(
            *[
                (
                    and_(
                        extract('month', Employer.date_of_birth) == month,
                        extract('day', Employer.date_of_birth) == day,
                    ),
                    i  # Присваиваем вес в зависимости от близости даты
                )
                for i, (month, day) in enumerate(day_month_pairs)
            ],
            else_=len(day_month_pairs)  # Все остальные дни рождения (если есть)
        )

        # Объединяем условия с помощью OR
        stmt = (
            select(Employer)
            .where(or_(*conditions))
            .order_by(
                order_by_case.asc(),  # Сначала ближайшие дни рождения
                extract('month', Employer.date_of_birth).asc(),
                extract('day', Employer.date_of_birth).asc(),
            )
            .offset(start)
            .limit(limit)
        )

        res = await self.session.execute(stmt)
        res = [row[0].to_read_model_for_birth() for row in res.all()]
        return res
