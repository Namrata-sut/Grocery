from enum import Enum

from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as sqlEnum

from app.core.db_connection import Base


class Role(Enum):
    admin = "admin"
    user = "user"


class UserModel(Base):
    __tablename__ = "user_table"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(sqlEnum(Role), default=Role.user)
