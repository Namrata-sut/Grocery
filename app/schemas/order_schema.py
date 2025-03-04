from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class OrderSchema(BaseModel):
    product_id: int
    quantity: int
    status: str
    ordered_date: Optional[datetime] = None
    total_price: Optional[float] = None

    @classmethod
    def from_orm(cls, order, product=None):
        """ Manually compute total_price when converting SQLAlchemy model to Pydantic """
        return cls(
            product_id=order.product_id,
            quantity=order.quantity,
            status=order.status,
            ordered_date=order.ordered_date,
            total_price=(order.quantity * product.price if product else 0.0)
        )

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy models


class UpdateOrderSchema(BaseModel):
    product_id: int
    quantity: int
    status: str


class PartialUpdateOrderSchema(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None