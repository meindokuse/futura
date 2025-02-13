from typing import Optional

from src.data.unitofwork import IUnitOfWork
from src.schemas.items import ProductCreate


class ProductService:

    async def get_list_products(self, uow: IUnitOfWork, page: int, limit: int,
                                type_product: Optional[str], location_name: str):
        async with uow:
            if type_product is None:
                products = await uow.product.find_all(page=page, limit=limit, location_name=location_name)
            else:
                products = await uow.product.find_all(page=page, limit=limit, type_product=type_product,
                                                      location_name=location_name)
            return products

    async def add_product(self, uow: IUnitOfWork, product: ProductCreate):
        data = product.model_dump()
        async with uow:
            await uow.product.add_one(data)
            await uow.commit()

    async def delete_product(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.product.delete_one(id=id)
            await uow.commit()
