from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from forum.base.models import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
