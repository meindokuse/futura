
from src.data.repository import SQLAlchemyRepository
from src.models.items import Card


class CardRepository(SQLAlchemyRepository):
    model = Card