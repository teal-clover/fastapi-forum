from typing import Annotated

from fastapi import APIRouter, Depends

from forum.comment import models
from forum.comment.controllers import CommentController

from . import schemas

router = APIRouter()


@router.post("/comments/", response_model=schemas.Comment, status_code=201)
async def create_comment_for_user(
    controller: Annotated[CommentController, Depends()], comment: schemas.CommentCreate
) -> models.Comment:
    return await controller.create(new_comment=comment)


@router.get("/comments/", response_model=list[schemas.Comment])
async def read_comments(
    controller: Annotated[CommentController, Depends()], skip: int = 0, limit: int = 100
) -> list[models.Comment]:
    comments = await controller.read_all(skip=skip, limit=limit)
    return comments
