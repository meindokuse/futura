from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Employer


class EmployerRepository(SQLAlchemyRepository):
    model = Employer

    # async def find_one_with_work_days(self,fio: str):
    #     result = await self.session.execute(
    #         select(self.model)
    #         .options(selectinload(Employer.work_days))
    #         .filter_by(fio=fio)
    #     )
    #     res = result.scalar_one_or_none()
    #     if res:
    #         return res.to_read_model_with_work_days()
    #     return None

    async def get_employees(
            self,
            page: int,  # Смещение для пагинации
            limit: int,  # Лимит записей на страницу
            sort_by: str = "fio",  # Поле для сортировки (по умолчанию "fio")
            sort_order: str = "asc",  # Порядок сортировки ("asc" или "desc")
            filter_by: dict = None,  # Фильтры в виде словаря
    ):
        filter_by = filter_by or {}  # Если None, заменяем на пустой словарь

        # Проверяем, что поле для сортировки существует
        if not hasattr(self.model, sort_by):
            raise AttributeError(f"Model {self.model.__name__} has no attribute '{sort_by}'.")

        # Определяем порядок сортировки
        order_by = getattr(self.model, sort_by).desc() if sort_order.lower() == "desc" else getattr(self.model,
                                                                                                    sort_by).asc()

        # Пагинация
        start = (page - 1) * limit

        # Генерируем список фильтров (игнорируя несуществующие поля)
        filters = [
            getattr(self.model, key) == value
            for key, value in filter_by.items()
            if hasattr(self.model, key)
        ]

        # Формируем запрос с использованием where() и применяем фильтры
        stmt = (
            select(self.model)
            .where(*filters)
            .order_by(order_by)
            .offset(start)
            .limit(limit)
        )

        # Выполняем запрос
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res




