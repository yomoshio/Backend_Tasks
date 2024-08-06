from passlib.context import CryptContext
from app.api.v1.user.models import User
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user_logic(username: str, password: str):
    if await User.exists(username=username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await User.create(username=username, password_hash=get_password_hash(password))
    return user


