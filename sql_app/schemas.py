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


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    # posts: list[Post] = []

    class Config:
        orm_mode = True