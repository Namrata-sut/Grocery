from typing import Optional
from pydantic import BaseModel


class UserInputSchema(BaseModel):
    name: str
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    name: str
    email: str
    role: str


class UserPartialUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None



class DataToken(BaseModel):
    email: Optional[str] = None