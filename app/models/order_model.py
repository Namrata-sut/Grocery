from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Computed, func
from app.core.db_connection import Base

class OrderModel(Base):
    __tablename__ = "order_table"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product_table.product_id'), nullable=False)
    quantity = Column(Integer, default=0)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default='pending')
    ordered_date = Column(DateTime(timezone=True), default=func.now())
