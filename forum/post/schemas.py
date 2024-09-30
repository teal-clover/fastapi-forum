from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int | None

    model_config = ConfigDict(from_attributes=True)
