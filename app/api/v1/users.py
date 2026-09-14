from fastapi import FastAPI
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schema.user import UserCreate , UserResponse , UserUpdate
from app.models.user import User
from fastapi import HTTPException , status
from sqlalchemy import select
from app.core.security import hash_password , verify_password

from app.service.user_services import create_user


router = APIRouter()


    
@router.post("/user" , response_model=UserResponse)
def create_user_route(
    user_data : UserCreate , 
    db : Session = Depends(get_session)
): 
    user  = create_user(db=db , user_data=user_data)
    
    return user 
    


@router.get("/user/{user_id}"   , response_model=UserResponse)
def get_user(
      user_id : int  ,
    db: Session  = Depends(get_session) 
  
): 
    
    user = db.get(User , user_id)
    
    if user is None : 
        raise HTTPException(
            status_code=404 , 
            detail="user not found"
        )
    
    return user


# api for getting all the user 
@router.get("/users" , response_model= list[UserResponse])
def getall_user(
    db: Session = Depends(get_session)
): 
    
    statement = select(User)
    
    result  = db.execute(statement)
    
    users = result.scalars().all()
    
    return users
    
# now modify api using the patch 

@router.patch("/user/{user_id}" , response_model=UserResponse)
def modify_user(
    user_id : int , 
    user_data : UserUpdate , 
    db : Session = Depends(get_session)
):
    
    user = db.get(User , user_id)
    
    if user is None : 
        raise HTTPException(
            status_code=404 , 
            detail="user not found"
        )
        
    if user.username is not None : 
        user.username = user_data.username
    
    if user.email is not None: 
        user.email  = user_data.email
    
    try :    
        db.commit()
        db.refresh(user)
    except :
        db.rollback()
        
        

    return user

@router.delete("/user/{user_id}" , status_code=status.HTTP_204_NO_CONTENT)
def modify_user(
    user_id : int , 
    db : Session = Depends(get_session)
):
    
    user = db.get(User , user_id)
    
    if user is None : 
        raise HTTPException(
            status_code=404 , 
            detail="user not found"
        )

    db.delete(user)
    db.commit()
  