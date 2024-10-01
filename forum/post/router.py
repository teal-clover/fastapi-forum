from typing import Annotated

from fastapi import APIRouter, Depends

from forum.base.exceptions import PostNotFoundException
from forum.base.http_exceptions import PostNotFoundHTTPException
from forum.post import models
from forum.post.controllers import PostController
from forum.user.dependencies import get_current_active_user
from forum.user.models import User

from . import schemas

router = APIRouter()


@router.post("/posts/", response_model=schemas.Post, status_code=201)
async def create_post_for_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    controller: Annotated[PostController, Depends()],
    post: schemas.PostCreate,
) -> models.Post:
    try:
        return await controller.create(post=post, user=current_user)
    except PostNotFoundException:
        raise PostNotFoundHTTPException()


@router.get("/posts/", response_model=list[schemas.Post])
async def read_posts(
    controller: Annotated[PostController, Depends()],
    skip: int = 0,
    limit: int = 100,
) -> list[models.Post]:
    posts = await controller.read_all(
        skip=skip,
        limit=limit,
    )
    return posts
