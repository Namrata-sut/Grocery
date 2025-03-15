from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_connection import get_db
from app.core.security import get_current_user
from app.schemas.user_schema import UserInputSchema
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/create_user/")
async def create_user(
    payload: UserInputSchema,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_current_user),
):
    try:
        user_added = await UserService.add(payload, db)
        return user_added
    except Exception as e:
        return f"Error: {e}"


@user_router.get("/get_user_by_id/{user_id}/")
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_current_user),
):
    try:
        user = await UserService.get_user_by_id(user_id, db)
        return user
    except Exception as e:
        return f"Error: {e}"
