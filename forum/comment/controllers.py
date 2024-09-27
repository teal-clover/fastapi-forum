from typing import Annotated

from fastapi import Depends

from forum.base.exceptions import CommentNotFoundException
from forum.comment import models, schemas
from forum.comment.repository import CommentRepository
from forum.user.dependencies import get_current_active_user
from forum.user.models import User


class CommentController:
    def __init__(
        self,
        repo: CommentRepository,
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
        self.repo = repo
        self.user = current_user

    async def create(self, new_comment: schemas.CommentCreate) -> models.Comment:
        return await self.repo.create(new_comment, self.user.id)

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        comments = await self.repo.read_all(skip=skip, limit=limit)
        print(comments)
        return comments

    async def read_one(self, comment_id: int) -> models.Comment:
        comment = await self.repo.read_one(comment_id)
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def update(
        self, comment_id: int, comment: schemas.CommentUpdate
    ) -> models.Comment:
        return await self.repo.update(item=comment, item_id=comment_id)

    async def delete(self, comment_id: int) -> models.Comment:
        return await self.repo.delete(item_id=comment_id)
