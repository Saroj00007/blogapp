from sqlalchemy.orm import Mapped ,mapped_column  , relationship
from app.db.base import Base

from sqlalchemy import String 


class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str]  = mapped_column(unique=True)
    password_hash : Mapped[str]
    
    posts = relationship(
        "Post" , 
        back_populates= "author"
    )
    
    
