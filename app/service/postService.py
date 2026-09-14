
from app.db.session import get_session
from app.schema.post import PostCreate , PostUpdate , PostResponse

from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.post import Post
from sqlalchemy import select , desc


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

def get_all_post(
    db: Session , 
    limit : int  , 
    skip : int  ,
    published : bool | None = None
    
):

   statement  = (select(Post).order_by(desc(Post.created_at))) # ordering this lets you return the recent post first the latest one is first 
  
   if published is not None : 
      statement = statement.where(
          Post.published == True
      )
    
   statement =(statement.offset(skip).limit(limit)) # limit and offset helps in pagination and other types of things 
   
   posts  = db.execute(statement)
   
   return list(posts.scalars().all())


# done xa now we will be working on updating the post 

def update_post(db: Session , post_data  : PostUpdate ,post : Post ) -> PostResponse:
    
    updated_data = post_data.model_dump(
        exclude_unset = True
    )
    
    for field  , value in updated_data.items():
        setattr(post, field , value)
    
    db.commit()
    db.refresh(post)
    
    
    return post

def delete_post(
    db: Session , 
    post : Post
): 
    db.delete(post)
    db.commit()
    
    
 
  



    
