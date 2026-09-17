from fastapi import APIRouter , status , Depends , HTTPException
from app.schema.comment import CommentResponse
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.user import User 
from app.dependencies.auth import get_current_user
from app.service.comment_service import create_comment , get_comment_byPostid
from app.schema.comment import CommentCreate , CommentResponse
from app.models.post import Post
from fastapi import Query



router = APIRouter()


@router.post("/post/{post_id}/comments" , response_model=CommentResponse , status_code=status.HTTP_201_CREATED)
def createComment(
    comment_data : CommentCreate , 
    post_id : int , 
    db : Session = Depends(get_session) , 
    current_user : User = Depends(get_current_user) , 
   
):

    post = db.get(Post , post_id )
    
    if post is None : 
        raise HTTPException(
            detail="post not found " , 
            status_code=404
        )
    
    comment = create_comment(
        post_id=post_id , 
        author_id=current_user.id, 
        db=db , 
        comment_data= comment_data
    )
    
    return comment

@router.get("/post/{post_id}/comments" , response_model=list[CommentResponse])
def getComments(
    post_id : int , 
    limit : int = Query(default=20), 
    skip : int = Query(default=0) , 
    db : Session  = Depends(get_session) ,
    )  :
    
    
    post = db.get(Post , post_id)
    
    if post is None : 
        raise HTTPException(
            detail= "post not found" , 
            status_code=404
        )

    comments = get_comment_byPostid(
        db=db , 
       post_id= post_id , 
       skip=skip ,
       limit=limit
    )
    
    
    return comments
    
    
    
    
    
    

