from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from forum.base.exceptions import (
    EmailTakenException,
    IncorectLoginInfoException,
    UserNotFoundException,
)
from forum.user import models, schemas
from forum.user.dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)
from forum.user.repository import UserRepository


class UserController:
    def __init__(
        self,
        repo: UserRepository,
    ):
        self.repo = repo

    async def create(self, new_user: schemas.UserCreate) -> models.User:
        user = await self.repo.read_one_by_email(email=new_user.email)
        if user:
            raise EmailTakenException
        return await self.repo.create(new_user)

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[models.User]:
        users = await self.repo.read_all(skip=skip, limit=limit)
        return users

    async def read_one(self, user_id: int) -> models.User:
        user = await self.repo.read_one(user_id)
        if not user:
            raise UserNotFoundException

        return user

    async def update(self, user_id: int, user: schemas.UserUpdate) -> models.User:
        return await self.repo.update(item=user, item_id=user_id)

    async def delete(self, user_id: int) -> models.User:
        return await self.repo.delete(item_id=user_id)


class AuthController:
    def __init__(
        self,
        repo: UserRepository,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
        self.repo = repo
        self.form_data = form_data

    async def authenticate(
        self,
    ) -> schemas.Token:
        user = await authenticate_user(
            repo=self.repo,
            email=self.form_data.username,
            password=self.form_data.password,
        )
        if not user:
            raise IncorectLoginInfoException
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return schemas.Token(access_token=access_token, token_type="bearer")
