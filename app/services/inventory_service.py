from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.order_schema import OrderSchema


class InventoryService:
    @staticmethod
    async def place_order(payload: OrderSchema, db: AsyncSession):
        order_obj = InventoryRepository(db)
        return await order_obj.place_order(payload)
