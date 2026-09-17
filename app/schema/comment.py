from pydantic import BaseModel , Field , ConfigDict

from datetime import datetime


class CommentCreate(BaseModel):
    content : str = Field(
        min_length=1 , 
        max_length=1000
    )
    
    
class CommentUpdate(BaseModel):
    content : str = Field(
        min_length=1 , 
        max_length=1000
    )
    
class CommentResponse(BaseModel):
    
     model_config = ConfigDict(from_attributes=True) # this ensure that the pydantic model wont't contradict with the sqlalchemy
    
     id : int 
     content : str
     author_id : int 
     post_id : int
     created_at : datetime 
     updated_at : datetime
       

