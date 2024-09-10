from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str | None = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int | None

    class Config:
        orm_mode = True
