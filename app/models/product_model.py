from sqlalchemy import Column, Float, Integer, String

from app.core.db_connection import Base


class ProductModel(Base):
    __tablename__ = "product_table"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
