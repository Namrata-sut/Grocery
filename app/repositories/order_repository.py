from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.order_model import OrderModel
from app.schemas.order_schema import OrderSchema, UpdateOrderSchema, PartialUpdateOrderSchema
from app.services.product_service import ProductService
from app.models.product_model import ProductModel


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, payload: OrderSchema):
        product = await ProductService.get_by_id(payload.product_id, self.db)
        data = OrderModel(
            product_id=payload.product_id,
            quantity=payload.quantity,
            status=payload.status,
            total_price=(payload.quantity * product.price)
        )
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)
        return data

    async def get_by_id(self, order_id: int):
        query = select(OrderModel).where(OrderModel.order_id == order_id)
        result = await self.db.execute(query)
        order = result.scalars().first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")
        return order

    async def get_all(self):
        result = await self.db.execute(select(OrderModel))
        orders = result.scalars().fetchall()
        return orders

    async def update(self, order_id: int, payload: UpdateOrderSchema):
        query = select(OrderModel).where(OrderModel.order_id == order_id)
        result = await self.db.execute(query)
        existing_order = result.scalars().first()
        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")

        product_id = payload.product_id

        query_product = select(ProductModel).where(ProductModel.product_id == product_id)
        product_result = await self.db.execute(query_product)
        product_existing = product_result.scalars().first()

        stock = product_existing.stock
        if int(stock) <= 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product out of stock.")

        if payload.quantity >= int(stock):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Only {stock} items left in stock, but you requested {payload.quantity}")

        price = product_existing.price

        if existing_order.quantity > payload.quantity:
            quantity = existing_order.quantity - payload.quantity
            product_existing.stock = product_existing.stock + quantity

        elif existing_order.quantity < payload.quantity:
            quantity = payload.quantity - existing_order.quantity
            product_existing.stock = product_existing.stock - quantity

        existing_order.total_price = price * payload.quantity
        # product_existing.stock = product_existing.stock - payload.quantity

        for key, value in payload.dict().items():
            setattr(existing_order, key, value)
        await self.db.commit()
        await self.db.refresh(existing_order)
        return existing_order

    async def partial_update(self, order_id: int, payload: PartialUpdateOrderSchema):

        query = select(OrderModel).where(OrderModel.order_id == order_id)
        result = await self.db.execute(query)
        existing_order = result.scalars().first()
        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")

        product_id = payload.product_id if payload.product_id is not None else existing_order.product_id

        if product_id:
            query_product = select(ProductModel).where(ProductModel.product_id == product_id)
            product_result = await self.db.execute(query_product)
            product_existing = product_result.scalars().first()
            price = product_existing.price

            if payload.quantity:
                if existing_order.quantity > payload.quantity:
                    quantity = existing_order.quantity - payload.quantity
                    product_existing.stock = product_existing.stock + quantity

                if existing_order.quantity < payload.quantity:
                    quantity = payload.quantity - existing_order.quantity
                    product_existing.stock = product_existing.stock - quantity

                existing_order.total_price = price * payload.quantity

        for key, value in payload.dict(exclude_unset=True).items():
            setattr(existing_order, key, value)
        await self.db.commit()
        await self.db.refresh(existing_order)
        return existing_order

    async def delete(self, order_id: int):
        query = select(OrderModel).where(OrderModel.order_id == order_id)
        result = await self.db.execute(query)
        existing_order = result.scalars().first()
        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found.")
        await self.db.delete(existing_order)
        await self.db.commit()
        return "Order deleted."
