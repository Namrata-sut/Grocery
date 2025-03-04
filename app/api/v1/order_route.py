from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_connection import get_db
from app.schemas.order_schema import OrderSchema, UpdateOrderSchema, PartialUpdateOrderSchema
from app.services.order_service import OrderService

router = APIRouter()

# {Product_id} inside the URL is a dynamic value. The value is extracted from the URL when the endpoint
# is called.


@router.get("/get_order_by_id/{order_id}")
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        order = await OrderService.get_by_id(order_id, db)
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.get("/get_all_orders")
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    try:
        orders = await OrderService.get_all(db)
        return orders
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.post("/add_new_order")
async def add_new_order(payload: OrderSchema, db: AsyncSession = Depends(get_db)):
    try:
        new_order = await OrderService.add(payload, db)
        return new_order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.put("/update_existing_order/{order_id}")
async def update_existing_order(order_id: int, payload: UpdateOrderSchema, db: AsyncSession=Depends(get_db)):
    try:
        updated_order = await OrderService.update(order_id, payload, db)
        return updated_order
    except Exception as e:
        return f"Error: {e}"


@router.patch("/partial_update_order/{order_id}")
async def partial_update_order(order_id: int, payload: PartialUpdateOrderSchema, db: AsyncSession=Depends(get_db)):
    try:
        updated_order = await OrderService.partial_update(order_id, payload, db)
        return updated_order
    except Exception as e:
        return f"Error: {e}"


@router.delete("/delete_existing_order/{order_id}")
async def delete_existing_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        product_deleted = await OrderService.delete(order_id, db)
        return product_deleted
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")
