from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repositories.product_repository import ProductRepository
from app.schemas.order_schema import OrderSchema
from app.schemas.product_schema import ProductPartialUpdateSchema
from app.services.order_service import OrderService


class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def place_order(self, payload: OrderSchema):
        await OrderService.add(payload, self.db)
        product_obj = ProductRepository(self.db)
        product = await product_obj.get_by_id(payload.product_id)
        if product.stock <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Product out of stock."
            )
        stock = product.stock - payload.quantity
        new_stock = ProductPartialUpdateSchema(stock=stock)
        await product_obj.partial_update(
            product_id=payload.product_id, payload=new_stock
        )
        return "Order Placed."
