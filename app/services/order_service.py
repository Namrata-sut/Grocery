from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderSchema, PartialUpdateOrderSchema, UpdateOrderSchema


class OrderService:
    @staticmethod
    async def add(payload: OrderSchema, db: AsyncSession):
        order_obj = OrderRepository(db)
        return await order_obj.add(payload)

    @staticmethod
    async def get_by_id(order_id: int, db: AsyncSession):
        order_obj = OrderRepository(db)
        return await order_obj.get_by_id(order_id)

    @staticmethod
    async def get_all(db: AsyncSession):
        order_obj = OrderRepository(db)
        return await order_obj.get_all()

    @staticmethod
    async def update(order_id: int, payload: UpdateOrderSchema, db: AsyncSession):
        order_obj = OrderRepository(db)
        return await order_obj.update(order_id, payload)

    @staticmethod
    async def partial_update(order_id: int, payload: PartialUpdateOrderSchema, db: AsyncSession):
        order_obj = OrderRepository(db)
        return await order_obj.partial_update(order_id, payload)

    @staticmethod
    async def delete(order_id: int, db: AsyncSession):
        order_obj = OrderRepository(db)
        return await order_obj.delete(order_id)
