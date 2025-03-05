from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_repository import ProductRepository
from app.schemas.order_schema import OrderSchema
from app.repositories.order_repository import OrderRepository
from app.schemas.product_schema import ProductPartialUpdateSchema


class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def place_order(self, payload: OrderSchema):
        order_obj = OrderRepository(self.db)
        await order_obj.add(payload)
        product_obj = ProductRepository(self.db)
        product = await product_obj.get_by_id(payload.product_id)
        stock = product.stock - payload.quantity
        new_stock = ProductPartialUpdateSchema(stock=stock)
        await product_obj.partial_update(product_id=payload.product_id, payload=new_stock)
        return "Order Placed."
