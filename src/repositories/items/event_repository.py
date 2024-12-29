from src.data.repository import SQLAlchemyRepository

from src.models.items import Events

class EventRepository(SQLAlchemyRepository):
    model = Events

