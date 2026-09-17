from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.schema.auth import loginSchema

from app.db.session import get_session

from app.service.user_services import authenticate_user 
from app.core.security import create_access_token



router = APIRouter()

@router.post("/login")
def login_user(login_data  :loginSchema , db : Session = Depends(get_session)):
    
    
    # authenticate garne tespaxi right output return garne.
    
    user = authenticate_user(
        db  = db , 
        login_data=login_data
    )
    
    access_token = create_access_token(user_id= user.id)
    
    
    return {
       "ascess_token"  : access_token , 
       "token_type"  :"Bearrer"
    }
    
    
    
    