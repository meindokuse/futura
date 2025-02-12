from typing import Optional

from fastapi import APIRouter, Query

from src.api.dependses import UOWDep
from src.schemas.items import ProductCreate
from src.services.product_service import ProductService

router = APIRouter(
    tags=['product'],
    prefix='/product',
)


@router.post('/admin/add_product')
async def add_product(uow: UOWDep, product: ProductCreate):
    product_service = ProductService()
    await product_service.add_product(uow=uow, product=product)
    return {
        "status": "success",
    }


@router.get('/{location_name}/get_list_products/')
async def get_list_products(location_name:str,uow: UOWDep, page: int, limit: int, type_product: Optional[str] = Query(None)):
    product_service = ProductService()

    list_products = await product_service.get_list_products(uow=uow, page=page, limit=limit, type_product=type_product)
    return list_products


@router.delete('/admin/delete_product')
async def delete_product(uow: UOWDep, id: int):
    product_service = ProductService()
    await product_service.delete_product(uow=uow, id=id)
    return {
        "status": "success",
    }
