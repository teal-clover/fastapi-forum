from typing import Annotated

from fastapi import Depends, HTTPException

from forum.post import models, schemas
from forum.user.models import User
from forum.post.repository import PostRepository
from forum.user.dependencies import get_current_active_user


class PostController:
    def __init__(self, repo: PostRepository, current_user: Annotated[User, Depends(get_current_active_user)]):
        self.repo = repo
        self.user = current_user

    async def create(self, post: schemas.PostCreate) -> models.Post:
        return await self.repo.create(post=post, user_id=self.user.id)

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[models.Post]:
        posts = await self.repo.read_all(skip=skip, limit=limit)
        return posts
