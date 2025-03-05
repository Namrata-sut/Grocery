from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db_connection import get_db
from app.schemas.order_schema import OrderSchema
from app.services.inventory_service import InventoryService

inventory_router = APIRouter()


@inventory_router.post("/place_order")
async def place_order(payload: OrderSchema, db: AsyncSession = Depends(get_db)):
    try:
        order_placed = await InventoryService.place_order(payload, db)
        return order_placed
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")
