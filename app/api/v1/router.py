from fastapi import FastAPI
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schema.user import UserCreate , UserResponse , UserUpdate
from app.models.user import User
from fastapi import HTTPException , status
from sqlalchemy import select
from app.service.postService import create_post , get_post
from app.schema.post import PostResponse , PostCreate


router = APIRouter()

@router.get("/health")
def health():
    return {"message" : "everything is fine"}

@router.get("/db_check")
def db_check(db : Session = Depends(get_session)):
    
    # now you can do the operation with db which is the session
    return { 
            "db" : db
            }
    
@router.post("/user" , response_model=UserResponse)
def create_user(
    user_data : UserCreate , 
    db : Session = Depends(get_session)
): 
    
    user = User(
        username  = user_data.username , 
        email = user_data.email , 
        password_hash = user_data.password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
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
  
  
# POST APIS 
@router.post("/post" , response_model=PostResponse , status_code= status.HTTP_201_CREATED)
def create_blog_post(
    post_data : PostCreate , 
    db: Session = Depends(get_session) ,    
): 
    
    post = create_post(
        db = db , 
        post_data= post_data , 
        author_id  = 1 # later when we implement authorization and authentication we will implement this authore id by extracting from token. 
    )
    
    
    return post


@router.get("/post/{post_id}" , response_model= PostResponse)
def get_post(
    post_id : int , 
    db : Session = Depends(get_session)
) : 
    
    post = get_post(
        post_id  =  post_id , 
        db = db
    )
    
    if post is None : 
        raise HTTPException(
            status_code=404 , 
            detail= "post not found! "
        )
    return post