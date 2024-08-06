from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.user.models import User_Pydantic, User
from app.api.v1.user import logic as l
from app.api.v1.user.schemas import UserCreate

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    response_model=User_Pydantic,
    summary="Register a User",
    description="Register a new user with a unique username and password.",
    response_description="The registered user."
)
async def register(user: UserCreate):
    return await l.create_user_logic(user.username, user.password)




