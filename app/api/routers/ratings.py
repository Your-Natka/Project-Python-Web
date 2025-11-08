from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.rating import RatingCreate, RatingResponse
from app.crud import rating as crud_rating
from app.deps import get_current_user  # Виправлено
from app.db.session import get_db

# Одне визначення router
router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse)
def create_rating(rating_in: RatingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Перевірка чи можна додати новий рейтинг
    rating = crud_rating.create_rating(db, rating_in, current_user.id)
    if not rating:
        raise HTTPException(status_code=400, detail="You have already rated this photo or not allowed")
    return rating

@router.get("/photo/{photo_id}", response_model=list[RatingResponse])
def get_ratings(photo_id: int, db: Session = Depends(get_db)):
    # Отримання рейтингів для певної фотографії
    return crud_rating.get_ratings_by_photo(db, photo_id)

@router.delete("/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Видалення рейтингу
    success = crud_rating.delete_rating(db, rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"detail": "Rating deleted"}
