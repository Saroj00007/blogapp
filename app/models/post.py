from pydantic import BaseModel  
from sqlalchemy.orm import Mapped  , mapped_column , relationship 

from sqlalchemy import Boolean , String , Text , DateTime , ForeignKey
from app.db.base import Base

from datetime import datetime


class Post(Base):
    
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    author = relationship(
        "User",
        back_populates="posts",
    )
    
    comments = relationship(
        "Comment" , 
        back_populates="comments"
    )