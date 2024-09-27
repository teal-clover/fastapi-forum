from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from forum.base.models import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    content: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
