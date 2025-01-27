from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.models.items import Product
from src.schemas.items import ProductCreate


class ProductService:

    async def get_list_products(self, uow: IUnitOfWork, page: int, limit: int,
                                type_product: Optional[str]):
        async with uow:
            products = uow.product.find_all(page=page, limit=limit, type_product=type_product)
            return products

    async def add_product(self, uow: IUnitOfWork, product: ProductCreate):
        async with uow:
            await uow.product.add_one(product)

    async def delete_product(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.product.delete_one(id=id)
