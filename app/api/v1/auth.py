from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_connection import get_db
from app.core.security import hash_password
from app.schemas.user_schema import UserInputSchema
from app.services.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(payload: UserInputSchema, db: AsyncSession = Depends(get_db)):
    try:
        hashed_password = hash_password(payload.password)
        payload.password = hashed_password
        user_added = await UserService.add(payload, db)
        return user_added
    except Exception as e:
        return f"Error: {e}"


@auth_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """Login endpoint that returns JWT token"""
    try:
        email = form_data.username
        password = form_data.password
        token = await UserService.get_user(str(email), str(password), db)
        if not token:
            return {"error": "Token has not created."}
        # response = Response(content="Login successful")
        # response.headers["Authorization"] = f"Bearer {token['access_token']}"
        return token
    except Exception as e:
        return f"Error: {e}"
