#  this contain all the services that the comment contain
from app.models.comments import Comment , Post , User
from sqlalchemy.orm import Session 
from fastapi import HTTPException 
from app.schema.comment import CommentCreate , CommentUpdate
from sqlalchemy import select 


# the service must be specific it must only perform what its designed to do 
def create_comment(post_id : int ,
                   author_id : int , 
                   db : Session , 
                   comment_data : CommentCreate
                   ) -> Comment:
    
    # comment created 
    comment  = Comment(
        content  = comment_data.content , 
        post_id  = post_id  , 
        author_id  = author_id
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment

# delete comment
def delete_comment(db: Session , 
                   comment : Comment
                   ): 
    
    # find the required comment through the comment_id 
       
    db.delete(comment)
    db.commit()
    
def update_comment(db : Session , 
                   comment_data : CommentUpdate , 
                   comment : Comment
                ): 
    
    comment_update  = comment_data.model_dump(
        exclude_unset= True
    ) # what it actually does is model dump convert the pydantic model into the python object and other things + so on
    
    for field , value in comment_update.items():
        setattr(comment , field , value)
    
    db.commit()
    db.refresh(comment)
    
    return comment  



def get_comment(db : Session , 
                comment_id : int
                )-> Comment:
    
    comment  = db.get(Comment , comment_id)
    
    if comment is None: 
        raise HTTPException(
            detail="comment not found" , 
            status_code=404
        )
    
    return comment

# getting the comment of the individual post

def get_comment_byPostid(
    db : Session , 
    post_id : int , 
    skip : int | None , 
    limit  :int | None
) -> list[Comment]:
    
  
  statement = (
      select(Comment).where(Comment.post_id == post_id).offset(skip).limit(limit=limit).order_by(Comment.created_at.asc())
  )
  
  result = db.execute(statement=statement)
  
  return list(result.scalars().all())