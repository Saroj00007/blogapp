
from app.db.session import get_session
from app.schema.post import PostCreate

from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.post import Post

def create_post(
    post_data : PostCreate , 
    db: Session  , 
    author_id : int
): 
    post = Post(
        title = post_data.title , 
        content = post_data.content , 
        published = post_data.published , 
        author_id  = author_id 
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post


def get_post(
    post_id : int , 
    db : Session 
): 
    return db.get(Post , post_id)


    
    