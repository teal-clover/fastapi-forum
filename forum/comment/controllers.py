from forum.base.exceptions import CommentNotFoundException, CredentialsException
from forum.comment import models, schemas
from forum.comment.repository import CommentRepository
from forum.user.models import User


class CommentController:
    def __init__(
        self,
        repo: CommentRepository,
    ):
        self.repo = repo

    async def create(
        self, new_comment: schemas.CommentCreate, user_id: int, post_id: int
    ) -> models.Comment:
        return await self.repo.create(new_comment, user_id, post_id)

    async def read_by_post_id(self, post_id: int) -> list[models.Comment]:
        comments = await self.repo.read_comments_by_post_id(post_id)
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

    async def delete(self, comment_id: int, user: User) -> None:
        comment = await self.repo.read_one(comment_id)
        if comment.user_id == user.id:
            await self.repo.delete(item_id=comment_id)
        else:
            raise CredentialsException()

    async def like_comment(self, comment_id: int, user: User) -> None:
        comment = await self.repo.toggle_like(comment_id=comment_id, user=user)
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def list_likes(self, comment_id: int) -> list[User]:
        users = await self.repo.read_likes(comment_id)
        if users is None:
            raise CommentNotFoundException()
        return users

    async def read_comments_by_user(self, user: User) -> list[models.Comment]:
        comments = await self.repo.read_comments_by_user_id(user.id)
        return comments
