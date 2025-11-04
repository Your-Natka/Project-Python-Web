from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.photo import Photo
from app.models.tag import Tag
from app.models.transformed_link import TransformedLink
from app.services import cloudinary_service, qr_services


# Створюємо фото
async def create_photo(db: AsyncSession,owner_id: int,cloudinary_data: dict,description: str,tag_names: Optional[List[str]] = None) -> Photo:
    tag_names = tag_names or []
    photo = Photo(
        owner_id=owner_id,
        cloudinary_public_id=cloudinary_data["public_id"],
        cloudinary_url=cloudinary_data["url"],
        description=description
    )

    # Додаємо теги
    for name in tag_names:
        # шукаємо тег у базі
        result = await db.execute(select(Tag).where(Tag.name == name))
        tag = result.scalars().first()
        if not tag:
            tag = Tag(name=name)
        photo.tags.append(tag)

    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo

# Отримуємо фото по slug
async def get_photo_by_slug(db: AsyncSession, slug: str) -> Optional[Photo]:
    result = await db.execute(select(Photo).where(Photo.unique_slug == slug))
    return result.scalars().first()


# Отримуємо фото по id
async def get_photo_by_id(db: AsyncSession, photo_id: int) -> Optional[Photo]:
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    return result.scalars().first()


# Оновлюємо фото
async def update_photo(db: AsyncSession, photo: Photo, description: Optional[str] = None, tag_names: Optional[List[str]] = None
) -> Photo:
    if description is not None:
        photo.description = description   # type: ignore

    if tag_names is not None:
        photo.tags.clear()
        for name in tag_names:
            result = await db.execute(select(Tag).where(Tag.name == name))
            tag = result.scalars().first()
            if not tag:
                tag = Tag(name=name)
            photo.tags.append(tag)

    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


# Видаляємо фото
async def delete_photo(db: AsyncSession, photo: Photo) -> None:
    await db.delete(photo)
    await db.commit()


async def search_photos(db: AsyncSession, keyword: Optional[str] = None, tag_name: Optional[str] = None
) -> List[Photo]:
    from app.models.tag import Tag
    query = select(Photo)
    if keyword:
        query = query.where(Photo.description.ilike(f"%{keyword}%"))
    if tag_name:
        query = query.join(Photo.tags).where(Tag.name == tag_name)
    result = await db.execute(query)
    return list(result.scalars().all())

async def transform_photo(db: AsyncSession, photo: Photo, current_user_id: int, width: Optional[int] = None,
    height: Optional[int] = None) -> TransformedLink:
    # Параметри трансформації
    transformation_params: Dict[str, Any] = {}
    if width:
        transformation_params["width"] = width
    if height:
        transformation_params["height"] = height

    # Cloudinary - трансформація
    transformed_url = cloudinary_service.create_transformed_url(
        str(photo.cloudinary_public_id), transformation_params
    )

    # Генерація QR-коду
    qr_url = qr_services.generate_qr_code(transformed_url, save_to="cloudinary")

    # Збереження у TransformedLink
    new_link = TransformedLink(
        photo_id=photo.id,
        transformation_params=transformation_params,
        url=transformed_url,
        qr_code_url=qr_url,
        created_by=current_user_id
    )
    db.add(new_link)
    await db.commit()
    await db.refresh(new_link)
    return new_link