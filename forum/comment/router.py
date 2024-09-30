from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from forum.base.exceptions import CredentialsException
from forum.comment import models
from forum.comment.controllers import CommentController
from forum.user.dependencies import get_current_active_user
from forum.user.models import User
from forum.user.schemas import User as UserScheme

from . import schemas

router = APIRouter()


@router.post("/comments/{post_id}", response_model=schemas.Comment, status_code=201)
async def create_comment_for_user(
    controller: Annotated[CommentController, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)],
    comment: schemas.CommentCreate,
    post_id: int,
) -> models.Comment:
    return await controller.create(
        new_comment=comment, user_id=current_user.id, post_id=post_id
    )


@router.get("/comments/post/{post_id}", response_model=list[schemas.Comment])
async def read_post_comments(
    controller: Annotated[CommentController, Depends()],
    post_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Comment]:
    comments = await controller.read_by_post_id(post_id=post_id)
    return comments


@router.get("/comments/likes/{comment_id}", response_model=list[UserScheme])
async def list_likes(
    controller: Annotated[CommentController, Depends()],
    comment_id: int,
) -> list[User]:
    return await controller.list_likes(comment_id=comment_id)


@router.post("/comments/likes/{comment_id}")
async def like_comment(
    controller: Annotated[CommentController, Depends()],
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    await controller.like_comment(comment_id=comment_id, user=current_user)


@router.get("/comments/user/{user_id}", response_model=list[schemas.Comment])
async def read_user_comments(
    controller: Annotated[CommentController, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> list[models.Comment]:
    return await controller.read_comments_by_user(user=current_user)


@router.put("/comments/{comment_id}", status_code=204)
async def update_comment(
    controller: Annotated[CommentController, Depends()],
    comment: schemas.CommentUpdate,
    comment_id: int,
) -> None:
    await controller.update(comment_id=comment_id, comment=comment)


@router.delete("/comments/{comment_id}", status_code=204)
async def delete_comment(
    controller: Annotated[CommentController, Depends()],
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    try:
        await controller.delete(comment_id=comment_id, user=current_user)
    except CredentialsException:
        raise HTTPException(detail="You don't have access!", status_code=401)
