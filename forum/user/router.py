from typing import Annotated

from fastapi import APIRouter, Depends, status

from forum.base.exceptions import (EmailTakenException,
                                   IncorectLoginInfoException)
from forum.base.http_exceptions import (EmailTakenHTTPException,
                                        IncorectLoginInfoHTTPException, UserNotFoundHTTPException)
from forum.user import models, schemas
from forum.user.controllers import AuthController, UserController
from forum.user.dependencies import get_current_active_user

router = APIRouter(prefix="/users")


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(
    controller: Annotated[UserController, Depends()], user: schemas.UserCreate
) -> models.User:
    try:
        return await controller.create(user)
    except EmailTakenException:
        raise EmailTakenHTTPException()


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
) -> models.User:
    return current_user


@router.get(path="/", response_model=list[schemas.User])
async def read_users(
    controller: Annotated[UserController, Depends()], skip: int = 0, limit: int = 100
) -> list[models.User]:
    return await controller.read_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def read_user(
    controller: Annotated[UserController, Depends()], user_id: int
) -> models.User:
    user = await controller.read_one(user_id=user_id)
    if not user:
        raise UserNotFoundHTTPException()
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    controller: Annotated[UserController, Depends()],
    user_id: int,
    user: schemas.UserUpdate,
) -> models.User:
    return await controller.update(user=user, user_id=user_id)


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
    controller: Annotated[UserController, Depends()], user_id: int
) -> models.User:
    return await controller.delete(user_id=user_id)


@router.post(path="/token")
async def login_for_access_token(
    controller: Annotated[AuthController, Depends()]
) -> schemas.Token:
    try:
        return await controller.authenticate()
    except IncorectLoginInfoException:
        raise IncorectLoginInfoHTTPException()
