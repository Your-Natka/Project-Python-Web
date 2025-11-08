from fastapi import (
    APIRouter, Depends, HTTPException, Query, status, UploadFile, File
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.db.session import get_db
from app.deps import get_current_user, require_role
from app.schemas.photo import PhotoCreate, PhotoOut, PhotoUpdate, PhotoTransformOut
from app.crud import photo as crud_photo
from app.services import cloudinary_service

router = APIRouter(prefix="/api/photos", tags=["Photos"])


# ------------------- UPLOAD PHOTO -------------------
@router.post("/upload", response_model=PhotoOut)
async def upload_photo(
    file: UploadFile = File(...),
    photo_in: PhotoCreate = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Завантажити нове фото.  
    Дозволено лише автентифікованим користувачам.
    """
    try:
        cloudinary_data = cloudinary_service.upload_image(file.file)
        photo = await crud_photo.create_photo(
            db=db,
            owner_id=current_user.user_id,
            cloudinary_data=cloudinary_data,
            description=photo_in.description or "",
            tag_names=photo_in.tags or []
        )
        return photo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------- GET PHOTO BY ID -------------------
@router.get("/{photo_id}", response_model=PhotoOut)
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати фото за ID.
    """
    photo = await crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


# ------------------- UPDATE PHOTO -------------------
@router.put("/{photo_id}", response_model=PhotoOut)
async def update_photo(
    photo_id: int,
    photo_in: PhotoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Оновити опис чи теги власного фото.
    """
    photo = await crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    if photo.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this photo")

    return await crud_photo.update_photo(
        db=db,
        photo=photo,
        description=photo_in.description,
        tag_names=photo_in.tags
    )


# ------------------- DELETE PHOTO -------------------
@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Видалити власне фото.
    """
    photo = await crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    if photo.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this photo")

    cloudinary_service.delete_image(str(photo.cloudinary_public_id))
    await crud_photo.delete_photo(db, photo)
    return {"detail": "Photo deleted successfully"}


# ------------------- TRANSFORM PHOTO -------------------
@router.post("/transform", response_model=PhotoTransformOut, status_code=status.HTTP_201_CREATED)
async def transform_photo(
    photo_id: int = Query(..., description="ID фото, яке потрібно трансформувати"),
    width: Optional[int] = Query(None),
    height: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("user"))
):
    """
    Виконати трансформацію фото (Cloudinary)  
    і створити QR-код для нового посилання.
    """
    photo = await crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    new_link = await crud_photo.transform_photo(
        db=db,
        photo=photo,
        current_user_id=current_user.user_id,
        width=width,
        height=height
    )

    return PhotoTransformOut(
        url=new_link.url,  # type: ignore
        qr_code_url=new_link.qr_code_url,  # type: ignore
        transformation_params=new_link.transformation_params  # type: ignore
    )


# ------------------- SEARCH -------------------
@router.get("/search", response_model=List[PhotoOut])
async def search_photos(
    keyword: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Пошук фото за ключовим словом або тегом.
    """
    return await crud_photo.search_photos(db, keyword=keyword, tag_name=tag)