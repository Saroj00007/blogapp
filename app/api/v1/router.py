from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.db.session import get_session

from app.api.v1 import posts  , users , auth  , comments


router = APIRouter()

router.include_router(
    users.router , 
    tags=['users']
)

router.include_router(
    posts.router , 
    tags=['posts']
)

router.include_router(
    auth.router , 
    tags=["login" , "authentication"]
)

@router.get("/health")
def health():
    return {"message" : "everything is fine"}

@router.get("/db_check")
def db_check(db : Session = Depends(get_session)):
    
    # now you can do the operation with db which is the session
    return { 
            "db" : db
            }

  

