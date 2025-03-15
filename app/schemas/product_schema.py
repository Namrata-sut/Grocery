from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    price: float
    stock: int

    class Config:
        from_attributes = True


class ProductUpdateSchema(BaseModel):
    name: str
    price: float
    stock: int


class ProductPartialUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
