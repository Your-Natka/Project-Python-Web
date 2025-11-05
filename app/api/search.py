from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc
from app.db.session import get_db
from app.models.photo import Photo
from app.models.tag import Tag
from app.models.rating import Rating
from app.schemas.photo import Photo  

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=list[Photo])
def search_photos(
    keyword: str | None = Query(None, description="Пошук за описом або назвою фото"),
    tag: str | None = Query(None, description="Пошук за тегом"),
    sort_by: str | None = Query(None, description="Сортувати за 'rating' або 'date'"),
    order: str | None = Query("desc", description="Порядок сортування: asc або desc"),
    db: Session = Depends(get_db)
):
    """
    Пошук і фільтрація фото за тегом, рейтингом або датою.
    """

    query = db.query(Photo)

    if keyword:
        query = query.filter(
            Photo.description.ilike(f"%{keyword}%") | Photo.title.ilike(f"%{keyword}%")
        )

    if tag:
        query = query.join(Photo.tags).filter(Tag.name.ilike(f"%{tag}%"))

    if sort_by == "rating":
        query = (
            query.outerjoin(Rating)
            .group_by(Photo.id)
            .add_columns(func.avg(Rating.value).label("avg_rating"))
        )
        query = query.order_by(asc("avg_rating") if order == "asc" else desc("avg_rating"))

    elif sort_by == "date":
        query = query.order_by(asc(Photo.created_at) if order == "asc" else desc(Photo.created_at))

    results = query.options(joinedload(Photo.tags)).all()

    if not results:
        raise HTTPException(status_code=404, detail="Фото не знайдено")

    return [item[0] if isinstance(item, tuple) else item for item in results]