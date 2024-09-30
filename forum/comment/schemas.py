from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: int
    content: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass
