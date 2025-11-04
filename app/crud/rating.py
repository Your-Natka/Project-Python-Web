from sqlalchemy.orm import Session
from app.models.rating import Rating
from app.schemas.rating import RatingCreate

def create_rating(db: Session, rating_data: RatingCreate, user_id: int):
    existing = db.query(Rating).filter(
        Rating.user_id == user_id, Rating.photo_id == rating_data.photo_id
    ).first()
    if existing:
        return None
    rating = Rating(**rating_data.dict(), user_id=user_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

def delete_rating(db: Session, rating_id: int):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
        return True
    return False

def get_ratings_by_photo(db: Session, photo_id: int):
    return db.query(Rating).filter(Rating.photo_id == photo_id).all()