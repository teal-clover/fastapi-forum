from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from forum.base.models import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    content: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
