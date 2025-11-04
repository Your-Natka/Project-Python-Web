from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.crud import comment as crud_comment
from app.deps.auth_deps import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
def create_comment(comment_in: CommentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_comment.create_comment(db, comment_in, user_id=current_user.id)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment_in: CommentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    comment = crud_comment.update_comment(db, comment_id, comment_in, current_user.id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or no permission")
    return comment

@router.get("/photo/{photo_id}", response_model=list[CommentResponse])
def get_comments(photo_id: int, db: Session = Depends(get_db)):
    return crud_comment.get_comments_by_photo(db, photo_id)