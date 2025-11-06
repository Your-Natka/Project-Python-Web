from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc
from app.db.session import get_db
from app.models.photo import Photo
from app.models.tag import Tag
from app.models.rating import Rating
from app.schemas.photo import PhotoOut
from app.docs.descriptions import search_description  # ✅ Імпорт із документації

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

@router.get(
    "/",
    response_model=list[PhotoOut],
    summary=search_description["search"]["summary"],
    description=search_description["search"]["description"],
    responses={
        200: {"description": "Успішний пошук фото"},
        404: {"description": "Фото не знайдено"},
        422: {"description": "Помилка у параметрах запиту"}
    },
)
async def search_photos(
    keyword: str | None = Query(None, description="Пошук за описом або назвою фото"),
    tag: str | None = Query(None, description="Пошук за тегом"),
    sort_by: str | None = Query(None, description="Сортувати за 'rating' або 'date'"),
    order: str | None = Query("desc", description="Порядок сортування: asc або desc"),
    limit: int = Query(10, ge=1, le=100, description="Кількість фото на сторінку"),
    offset: int = Query(0, ge=0, description="Зсув для пагінації"),
    db: Session = Depends(get_db)
):
    """
    🔍 Пошук і фільтрація фото за тегом, описом, рейтингом або датою.
    Підтримується пагінація через параметри `limit` і `offset`.
    """

    # 1️⃣ Базовий запит до таблиці Photo
    query = db.query(Photo)

    # 2️⃣ Фільтрація за ключовим словом (опис або slug)
    if keyword:
        query = query.filter(
            Photo.description.ilike(f"%{keyword}%") |
            Photo.unique_slug.ilike(f"%{keyword}%")
        )

    # 3️⃣ Фільтрація за тегом
    if tag:
        query = query.join(Photo.tags).filter(Tag.name.ilike(f"%{tag}%"))

    # 4️⃣ Сортування результатів
    if sort_by == "rating":
        query = (
            query.outerjoin(Rating)
            .group_by(Photo.id)
            .add_columns(func.avg(Rating.value).label("avg_rating"))
        )
        query = query.order_by(asc("avg_rating") if order == "asc" else desc("avg_rating"))
    elif sort_by == "date":
        query = query.order_by(
            asc(Photo.created_at) if order == "asc" else desc(Photo.created_at)
        )

    # 5️⃣ Пагінація
    query = query.offset(offset).limit(limit)

    # 6️⃣ Виконання запиту
    results = query.options(joinedload(Photo.tags)).all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фото не знайдено"
        )

    # 7️⃣ Якщо є join із рейтингом, результат буде кортежем (Photo, avg_rating)
    photos = [item[0] if isinstance(item, tuple) else item for item in results]

    return photos
