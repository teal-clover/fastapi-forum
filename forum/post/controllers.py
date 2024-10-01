from forum.base.exceptions import PostNotFoundException
from forum.post import models, schemas
from forum.post.repository import PostRepository
from forum.user.models import User


class PostController:
    def __init__(
        self,
        repo: PostRepository,
    ):
        self.repo = repo

    async def create(self, post: schemas.PostCreate, user: User) -> models.Post:
        post = await self.repo.create(item=post, user_id=int(user.id))
        return post

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[models.Post]:
        posts = await self.repo.read_all(skip=skip, limit=limit)
        return posts
