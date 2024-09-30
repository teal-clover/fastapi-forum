from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum.base.models import Base
from forum.user.models import User

likes_association = Table(
    "comments_users",
    Base.metadata,
    Column("comment_id", ForeignKey("comments.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    likes: Mapped[list[User]] = relationship(secondary=likes_association)
