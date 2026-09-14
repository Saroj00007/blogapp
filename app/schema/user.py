from pydantic import BaseModel  , EmailStr , ConfigDict

class UserCreate(BaseModel):
    username : str 
    email : EmailStr 
    password : str
    
class UserResponse(BaseModel): 
    model_config = ConfigDict(from_attributes=True)  # this tells the pydantic that it is ok if the data come from sqlalchemy model
    
    id : int 
    username : str
    email : EmailStr
    
class UserUpdate(BaseModel):
    username : str 
    email : EmailStr
    
    