from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.schema.auth import loginSchema

from app.db.session import get_session

from app.service.user_services import authenticate_user


router = APIRouter()

@router.post("/login")
def login_user(login_data  :loginSchema , db : Session = Depends(get_session)):
    
    
    # authenticate garne tespaxi right output return garne.
    
    user = authenticate_user(
        db  = db , 
        login_data=login_data
    )
    
    
    return {
        "message " : "logged in succesfully"
    }
    
    