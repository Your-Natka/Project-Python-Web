from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Dict, Any, List
from app.db.session import get_db
from app.models.photo import Photo
from app.models.transformed_link import TransformedLink
from app.schemas.photo import PhotoTransformOut
from app.services import cloudinary_service, qr_services
from app.deps import get_current_user, require_role
from app.schemas.photo import PhotoCreate, PhotoOut, PhotoUpdate, PhotoTransformOut
from app.crud.photo import create_photo

router = APIRouter()

# POST /photos/ - завантажити фото
@router.post("/", response_model=PhotoOut)
async def upload_photo(
    file: UploadFile = File(...),
    photo_in: PhotoCreate = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        cloudinary_data = cloudinary_service.upload_image(file.file)
        photo = await create_photo(
            db=db,
            owner_id=current_user.user_id,
            cloudinary_data=cloudinary_data,
            description=photo_in.description or "",
            tag_names=photo_in.tags or []
        )
        return photo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# GET /photos/{slug} - отримати фото за slug
@router.get("/{slug}", response_model=PhotoOut)
async def get_photo(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo).where(Photo.unique_slug == slug))
    photo = result.scalars().first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

# PUT /photos/{id} - редагувати опис та теги
@router.put("/{photo_id}", response_model=PhotoOut)
async def update_photo(
    photo_id: int,
    photo_in: PhotoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalars().first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this photo")

    photo.description = photo_in.description or photo.description  # type: ignore

    if photo_in.tags is not None:
        from app.models.tag import Tag
        photo.tags.clear()
        for name in photo_in.tags:
            result_tag = await db.execute(select(Tag).where(Tag.name == name))
            tag = result_tag.scalars().first()
            if not tag:
                tag = Tag(name=name)
            photo.tags.append(tag)

    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo

# DELETE /photos/{id} - видалити фото
@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalars().first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this photo")

    cloudinary_service.delete_image(str(photo.cloudinary_public_id))
    await db.delete(photo)
    await db.commit()
    return {"detail": "Photo deleted successfully"}

# POST /photos/{id}/transform - трансформація + QR
@router.post(
    "/photos/{photo_id}/transform",
    response_model=PhotoTransformOut,
    status_code=status.HTTP_201_CREATED,
)
async def transform_photo(
    photo_id: int,
    width: Optional[int] = Query(None),
    height: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("user")),
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    transformation_params: Dict[str, Any] = {}
    if width:
        transformation_params["width"] = width
    if height:
        transformation_params["height"] = height

    transformed_url = cloudinary_service.create_transformed_url(
        str(photo.cloudinary_public_id), transformation_params
    )
    qr_url = qr_services.generate_qr_code(transformed_url, save_to="cloudinary")

    new_link = TransformedLink(
        photo_id=photo.id,
        transformation_params=transformation_params,
        url=transformed_url,
        qr_code_url=qr_url,
        created_by=current_user.user_id
    )
    db.add(new_link)
    await db.commit()
    await db.refresh(new_link)

    return PhotoTransformOut(
        url=transformed_url,
        qr_code_url=qr_url,
        transformation_params=transformation_params
    )

# GET /photos/search - пошук і фільтрація
@router.get("/search", response_model=List[PhotoOut])
async def search_photos(
    keyword: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select
    from app.models.tag import Tag
    query = select(Photo)
    if keyword:
        query = query.where(Photo.description.ilike(f"%{keyword}%"))
    if tag:
        query = query.join(Photo.tags).where(Tag.name == tag)

    result = await db.execute(query)
    return result.scalars().all()


from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_photos():
    return {"message": "List of photos"}
