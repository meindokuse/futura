from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Employer


class EmployerRepository(SQLAlchemyRepository):
    model = Employer
