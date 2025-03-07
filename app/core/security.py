from datetime import datetime, UTC, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.user_schema import DataToken
from app.core.db_connection import get_db
from app.models.user_model import UserModel, Role

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ACCESS_TOKEN_EXPIRE_MINUTES = 40
SECRETE_KEY = 'grocery_management_secrete'
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_token(data: dict):
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(data, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("email")
        if not email:
            raise cred_exception
        return DataToken(email=email)

    except JWTError as e:
        print(f"JWT Error: {e}")
        raise cred_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the current authenticated user from the token in headers.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    token_data = verify_access_token(token, credentials_exception)
    if not token_data:
        raise credentials_exception

    user = await db.execute(select(UserModel).where(UserModel.email == token_data.email))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


async def admin_only(user_data=Depends(get_current_user)):
    """"""
    # try:
    breakpoint()
    if user_data.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized.")
    return user_data
    #
    # except Exception as e:
    #     return f"Error: {e}"
