from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from forum.base.database import get_session
from forum.base.repository import RepositoryBase
from forum.comment import schemas
from forum.comment.models import Comment
from forum.user.models import User


class CommentDBRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[Comment]:
        statement = select(Comment).offset(skip).limit(limit)
        response = await self.session.execute(statement)
        comments = response.scalars().all()
        return comments

    async def read_one(self, item_id: int) -> Comment | None:
        statement = select(Comment).filter(Comment.id == item_id)
        response = await self.session.execute(statement)
        comment = response.scalar_one_or_none()
        return comment

    async def toggle_like(self, comment_id: int, user: User) -> Comment | None:
        comment = await self.read_one(comment_id)
        if not comment:
            return None
        likes: list[User] = await comment.awaitable_attrs.likes
        if user not in likes:
            comment.likes.append(user)
        else:
            comment.likes.remove(user)
        self.session.add(comment)
        await self.session.commit()
        return comment

    async def create(
        self, item: schemas.CommentCreate, user_id: int, post_id: int
    ) -> Comment:
        comment = Comment(content=item.content, user_id=user_id, post_id=post_id)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def update(self, item_id: int, item: schemas.CommentUpdate) -> Comment:
        comment = await self.read_one(item_id)
        comment.content = item.content
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def delete(self, item_id: int) -> Comment:
        comment = await self.read_one(item_id)
        await self.session.delete(comment)
        await self.session.commit()
        return comment

    async def read_comments_by_post_id(self, post_id: int) -> list[Comment]:
        statement = select(Comment).filter(Comment.post_id == post_id)
        response = await self.session.execute(statement)
        comments = response.scalars().all()
        return comments

    async def read_likes(self, comment_id: int) -> list[User] | None:
        comment = await self.read_one(comment_id)
        if not comment:
            return None
        likes: list[User] = await comment.awaitable_attrs.likes
        return likes

    async def read_comments_by_user_id(self, user_id: int) -> list[Comment]:
        statement = select(Comment).filter(Comment.user_id == user_id)
        response = await self.session.execute(statement)
        comments = response.scalars().all()
        return comments


def get_comment_repository():
    def func(session: AsyncSession = Depends(get_session)):
        return CommentDBRepository(session)

    return func


CommentRepository = Annotated[CommentDBRepository, Depends(get_comment_repository())]
