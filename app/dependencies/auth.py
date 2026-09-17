from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , status
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.core.security import decode_token
from app.models.user import User


Oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login"
)


def get_current_user(
    token  : str = Depends(Oauth2_schema) , 
    db  : Session = Depends(get_session)
):
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED , 
        detail="could not validate credential" , 
        headers={"WWW-Authenticate"  :"Bearer"}
    )
    
    try: 
       
       payload = decode_token(token=token)
       
       user_id  = payload.get("sub")
       
       if user_id is None:
           raise credential_exception
       
       user = db.get(User  , user_id)
       
       if user is None : 
           raise credential_exception
    
    except(ValueError  , TypeError , Exception):
        raise credential_exception
    
    
    return user
        
    

