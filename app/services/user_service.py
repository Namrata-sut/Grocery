from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserInputSchema


class UserService:
    @staticmethod
    async def add(payload: UserInputSchema, db: AsyncSession):
        user_obj = UserRepository(db)
        user_added = await user_obj.add(payload)
        return user_added

    @staticmethod
    async def get_user(email: str, password: str, db: AsyncSession):
        user_obj = UserRepository(db)
        token = await user_obj.get_user(email, password)
        return token

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession):
        user_obj = UserRepository(db)
        user = await user_obj.get_user_by_id(user_id)
        return user
