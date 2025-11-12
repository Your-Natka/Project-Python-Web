# from sqlalchemy.orm import Session
# from app.models.comment import Comment
# from app.schemas.comment import CommentCreate, CommentUpdate

# def create_comment(db: Session, comment_data: CommentCreate, user_id: int):
#     comment = Comment(**comment_data.dict(), user_id=user_id)
#     db.add(comment)
#     db.commit()
#     db.refresh(comment)
#     return comment

# def update_comment(db: Session, comment_id: int, comment_data: CommentUpdate, user_id: int):
#     comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
#     if not comment:
#         return None
#     comment.content = comment_data.content
#     db.commit()
#     db.refresh(comment)
#     return comment

# def delete_comment(db: Session, comment_id: int):
#     comment = db.query(Comment).filter(Comment.id == comment_id).first()
#     if comment:
#         db.delete(comment)
#         db.commit()
#         return True
#     return False

# def get_comments_by_photo(db: Session, photo_id: int):
#     return db.query(Comment).filter(Comment.photo_id == photo_id).all()