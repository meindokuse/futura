from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.models.items import Product


class ProductService:

    async def get_list_products(self, uow: IUnitOfWork, page: int, limit: int,
                               type_product: Optional[str]):
        async with uow:
            products = uow.product.find_all(page=page, limit=limit, type_product=type_product)
            return products

    async def add_product(self, uow: IUnitOfWork, product: Product):
        async with uow:
            await uow.product.add_one(product)

