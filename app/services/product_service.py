from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import (
    ProductPartialUpdateSchema,
    ProductSchema,
    ProductUpdateSchema,
)


class ProductNotFoundError(HTTPException):
    def __init__(self, product_id: int = None, product_name: str = None):
        self.product_id = product_id
        if product_id:
            self.detail = f"Product with Id {product_id} not found."
        elif product_name:
            self.detail = f"Product with Name {product_name} doesn't exist."
        else:
            self.detail = "Product not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)


class EmptyProductTableError(HTTPException):
    def __init__(self):
        self.detail = "Product Table is empty."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)


class ProductService:
    @staticmethod
    async def add(payload: ProductSchema, db: AsyncSession):
        product_obj = ProductRepository(db)
        return await product_obj.add(payload)

    @staticmethod
    async def get_by_id(product_id: int, db: AsyncSession):
        product_obj = ProductRepository(db)
        return await product_obj.get_by_id(product_id)

    @staticmethod
    async def get_by_name(product_name: str, db: AsyncSession):
        product_obj = ProductRepository(db)
        return await product_obj.get_by_name(product_name)

    @staticmethod
    async def get_all(db: AsyncSession):
        product_obj = ProductRepository(db)
        return await product_obj.get_all()

    @staticmethod
    async def update(product_id: int, payload: ProductUpdateSchema, db: AsyncSession):
        product_obj = ProductRepository(db)
        return await product_obj.update(product_id, payload)

    @staticmethod
    async def partial_update(
        product_id: int, payload: ProductPartialUpdateSchema, db: AsyncSession
    ):
        product_obj = ProductRepository(db)
        return await product_obj.partial_update(product_id, payload)

    @staticmethod
    async def delete(product_id: int, db: AsyncSession):
        product_obj = ProductRepository(db)
        return await product_obj.delete(product_id)
