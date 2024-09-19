from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from forum.user import models, schemas
from forum.user.controllers import UserController
from forum.user.dependencies import (ACCESS_TOKEN_EXPIRE_MINUTES,
                                     authenticate_user, create_access_token,
                                     get_current_active_user)
from forum.user.repository import UserRepository

router = APIRouter(prefix="/users")


@router.post(path="/", status_code=201, response_model=schemas.User)
async def create_user(controller: Annotated[UserController, Depends()], user: schemas.UserCreate) -> schemas.User:
    return await controller.create(user)


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
) -> schemas.User:
    return current_user


@router.get(path="/", response_model=list[schemas.User])
async def read_users(controller: Annotated[UserController, Depends()], skip: int = 0, limit: int = 100) -> list[schemas.User]:
    return await controller.read_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User, status_code=200)
async def read_user(controller: Annotated[UserController, Depends()], user_id: int) -> schemas.User:
    return await controller.read_one(user_id=user_id)


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(controller: Annotated[UserController, Depends()], user_id: int, user: schemas.UserUpdate) -> schemas.User:
    return await controller.update(user=user, user_id=user_id)


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(controller: Annotated[UserController, Depends()], user_id: int) -> schemas.User:
    return await controller.delete(user_id=user_id)


@router.post(path="/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: UserRepository
) -> schemas.Token:
    user = await authenticate_user(repo=repo,
                                   email=form_data.username,
                                   password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
