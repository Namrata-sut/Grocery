from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import ProductModel
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


class ProductRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def add(self, payload: ProductSchema):
        data = ProductModel(name=payload.name, price=payload.price, stock=payload.stock)
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)
        return data

    async def get_by_id(self, product_id: int):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await self.db.execute(query)
        product = result.scalars().first()

        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return product

    async def get_by_name(self, product_name: str):
        query = select(ProductModel).where(
            func.lower(ProductModel.name) == product_name.lower()
        )
        result = await self.db.execute(query)
        products = result.scalars().all()

        if not products:
            raise ProductNotFoundError(product_name=product_name)
        return products

    async def get_all(self):
        query = select(ProductModel)
        result = await self.db.execute(query)
        products = result.scalars().all()
        if not products:
            raise EmptyProductTableError
        return products

    async def update(self, product_id: int, payload: ProductUpdateSchema):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await self.db.execute(query)
        existing_product = result.scalars().first()

        if not existing_product:
            raise ProductNotFoundError(product_id=product_id)
        for key, value in payload.dict().items():
            setattr(existing_product, key, value)

        await self.db.commit()
        await self.db.refresh(existing_product)
        return existing_product

    async def partial_update(
        self, product_id: int, payload: ProductPartialUpdateSchema
    ):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await self.db.execute(query)
        existing_product = result.scalars().first()
        if not existing_product:
            raise ProductNotFoundError(product_id=product_id)

        for key, value in payload.dict(exclude_unset=True).items():
            setattr(existing_product, key, value)

        await self.db.commit()
        await self.db.refresh(existing_product)
        return existing_product

    async def delete(self, product_id: int):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await self.db.execute(query)
        product = result.scalars().first()
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        await self.db.delete(product)
        await self.db.commit()
        return "product deleted"
