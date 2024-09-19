from fastapi import HTTPException

from forum.user import models, schemas
from forum.user.repository import UserRepository


class UserController:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create(self, user: schemas.UserCreate) -> models.User:
        db_user = await self.repo.read_one_by_email(email=user.email)
        if db_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")
        return await self.repo.create(user)

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[models.User]:
        users = await self.repo.read_all(skip=skip, limit=limit)
        return users

    async def read_one(self, user_id: int) -> models.User:
        db_user = await self.repo.read_one(user_id)
        return db_user

    async def update(self, user_id: int, user: schemas.UserUpdate) -> models.User:
        return await self.repo.update(user=user, user_id=user_id)

    async def delete(self, user_id: int) -> models.User:
        return await self.repo.delete(user_id=user_id)
