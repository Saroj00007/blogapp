from pwdlib import PasswordHash
from datetime import datetime , timedelta  , timezone

import jwt 
from app.core.config import settings



password_hash = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password=password )

def verify_password(password : str , hash_password : str) -> bool:
    return password_hash.verify(password , hash_password  )


def create_access_token(user_id : int):
    
    expire = datetime.now(timezone.utc)  + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    
    payload = {
        "sub"  : str(user_id) , 
        "exp"  :expire
    }
    
    token = jwt.encode(
        payload , 
        settings.jwt_secret_key , 
        algorithm= settings.jwt_algorithm
    )
    
    return token

    # first ma payload  , expiry time -> and then alogrithm 

def decode_token(token : str):
    
    decoded_token = jwt.decode(
        token , 
        settings.jwt_secret_key , 
        algorithms=[settings.jwt_algorithm]
    )

    return decoded_token



