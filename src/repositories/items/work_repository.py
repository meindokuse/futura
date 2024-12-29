from src.data.repository import SQLAlchemyRepository
from src.models.items import EmployerInWorkDay


class WorkRepository(SQLAlchemyRepository):
    model = EmployerInWorkDay
