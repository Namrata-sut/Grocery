from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import create_token, verify_password
from app.models.user_model import UserModel
from app.schemas.user_schema import UserInputSchema


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, payload: UserInputSchema):
        data = UserModel(
            name=payload.name, email=payload.email, password=payload.password
        )
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)
        result = data.__dict__
        return result

    async def get_user_by_id(self, user_id: int):
        query = select(UserModel).where(UserModel.user_id == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist."
            )
        return user

    async def get_user(self, email: str, password: str):
        query = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist."
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password does not match",
            )
        access_token = create_token(data={"user_id": user.user_id, "email": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
