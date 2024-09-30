from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum.base.models import Base
from forum.comment.models import Comment


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    comment: Mapped[list[Comment]] = relationship()
