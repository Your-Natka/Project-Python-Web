from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.crud import comment as crud_comment
from app.deps import get_current_user
from app.db.session import get_db
from app.docs.descriptions import comments_description  # ✅ імпортуємо описи

router = APIRouter(prefix="/api/comments", tags=["Comments"])

@router.post(
    "/photos/{photo_id}/comments/",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary=comments_description["create_comment"]["summary"],
    description=comments_description["create_comment"]["description"]
)
async def create_comment(
    photo_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    comment_in.photo_id = photo_id
    comment = await crud_comment.create_comment(db, comment_in, user_id=current_user.user_id)
    if not comment:
        raise HTTPException(status_code=400, detail="Unable to create comment")
    return comment


@router.put(
    "/comments/{comment_id}/",
    response_model=CommentResponse,
    summary=comments_description["update_comment"]["summary"],
    description=comments_description["update_comment"]["description"]
)
async def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    comment = await crud_comment.update_comment(db, comment_id, comment_in, current_user.user_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or no permission")
    return comment


@router.delete(
    "/comments/{comment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=comments_description["delete_comment"]["summary"],
    description=comments_description["delete_comment"]["description"]
)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = await crud_comment.delete_comment(db, comment_id, current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or no permission")
    return {"detail": "Comment deleted"}


@router.get(
    "/photos/{photo_id}/comments/",
    response_model=list[CommentResponse],
    summary=comments_description["get_comments"]["summary"],
    description=comments_description["get_comments"]["description"]
)
async def get_comments(photo_id: int, db: Session = Depends(get_db)):
    return await crud_comment.get_comments_by_photo(db, photo_id)
