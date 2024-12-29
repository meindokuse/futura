
from src.data.repository import SQLAlchemyRepository
from src.models.items import Product


class ProductRepository(SQLAlchemyRepository):
    model = Product