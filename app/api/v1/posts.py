from fastapi import FastAPI
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from fastapi import HTTPException , status
from sqlalchemy import select
from app.service.postService import create_post , get_post , get_all_post , update_post , delete_post
from app.schema.post import PostResponse , PostCreate


router = APIRouter()

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
def get_post_1(
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


@router.get("/posts" ,response_model=list[PostResponse])
def get_allRequest( limit: int = 10 , skip: int  = 0 ,published : bool | None = True ,  db : Session = Depends(get_session) ):
    
    posts  = get_all_post(db=db , limit=limit , skip=skip , published=published)
    
    if posts is None: 
        raise HTTPException(
            detail="posts not found" , 
            status_code= 404
        )
    
    
    return posts

@router.patch("/post/{post_id}" , response_model=PostResponse)
def updated_post(
    post_id  :int , 
    db : Session = Depends(get_session) , 
): 
    post = get_post(db=db ,post_id=post_id )
    
    if post is None : 
        raise HTTPException(
            detail = "post not found" , 
            status_code=404
        )
        
    
    return update_post(
        db = db  , 
        post_data = post , 
        post_id = post_id
    )
    
@router.delete("/post/{post_id}"  , status_code=status.HTTP_204_NO_CONTENT)
def deleted_post(post_id : int ,db : Session = Depends(get_session) ):
    
    post = db.get(post , post_id)
    if post is None:
        raise HTTPException(
            detail="post not found"  , 
            status_code= 404
        )
    
    delete_post(db=db , post=post)
    
    
    
    
    
    
    
    
    
    
    
    
    
    

