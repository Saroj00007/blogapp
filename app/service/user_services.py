from fastapi import FastAPI  , HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import select

from app.models.user import User

from app.schema.user import UserCreate
from app.core.security import hash_password , verify_password

from app.schema.auth import loginSchema

def create_user(
    db : Session , 
    user_data : UserCreate
):
    user = User(
        username  = user_data.username , 
        email = user_data.email , 
        password_hash = hash_password( password = user_data.password)
    )
    
    
    if user is None: 
        raise HTTPException(
            detail= "unable to register the password" , 
            status_code=500
        )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def get_user_byEmail(email: str , db: Session):
    
    statement = select(User).where(User.email == email)
    
    user = db.execute(statement)
    
    return user.scalar_one_or_none() # scalar one or none makes user that it return only one email / None


def authenticate_user(db: Session ,login_data : loginSchema ):
    
    user = get_user_byEmail(
        db = db , 
        email=login_data.email
    )
    
    if user is None :
        raise HTTPException(detail="invalid user name or password" , status_code=300)
    
    
    if not verify_password(
        login_data.password , 
        user.password_hash
    ) :
        raise HTTPException(
            detail="invalid username or password" , 
            status_code=300
        )
        
    return user
    
    
    
    
    
    