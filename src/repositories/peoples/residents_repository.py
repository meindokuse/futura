from src.data.repository import SQLAlchemyRepository
from src.models.peoples import Residents


class ResidentsRepository(SQLAlchemyRepository):
    model = Residents


