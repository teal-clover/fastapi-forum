from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum.base.models import Base
from forum.comment.models import Comment
from forum.post.models import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped[list[Post]] = relationship()
    comment: Mapped[list[Comment]] = relationship()
