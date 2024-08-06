from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import app.api.v1.auth.logic as auth_logic
import app.api.v1.auth.schemas as auth_schemas

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=auth_schemas.Token, summary="Login and get access token",
             description="Authenticate user and return a JWT token.", response_description="A JWT token for user.")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_logic.login_for_access_token(form_data)
