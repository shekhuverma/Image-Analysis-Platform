from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.db import services
from src.schemas import user
from src.security.jwt import create_access_token
from src.security.utils import authenticate_user
from src.settings import JWT_config

router = APIRouter(tags=["Users"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[any, Depends(services.save_db)],
):
    """
    User Login

    - **Raises:**
        - HTTPException: 401 if Incorrect username or password

    - **Returns:** {"access_token": access_token, "token_type": "bearer"}
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=JWT_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
async def sign_up(
    db: Annotated[any, Depends(services.save_db)],
    new_user: user.CreateUser,
):
    """
    Signup for new user

    - **Raises:**
        - HTTPException: 400 if Incorrect username already exist

    """
    user_exists = await services.get_user(new_user.username, db)
    if user_exists:
        raise HTTPException(
            400, detail=f"User with username {new_user.username} already exists!"
        )

    _, created_user = await services.create_user(new_user, db)

    return {f"Created user with username = {created_user.username}"}
