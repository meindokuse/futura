from src.data.repository import SQLAlchemyRepository
from src.models.items import Location


class LocationRepository(SQLAlchemyRepository):
    model = Location