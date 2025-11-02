from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.photo import Photo
from app.models.tag import Tag
from app.models.transformed_link import TransformedLink

async def create_photo(db: AsyncSession, owner_id: int, cloudinary_data: dict, description: str, tag_names: list):
    # Створюємо фото
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
