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
from app.crud import photo as crud_photo
from app.services import cloudinary_service, qr_services


router = APIRouter()


# POST /photos/ - завантажити фото
@router.post("/", response_model=PhotoOut)
async def upload_photo(file: UploadFile = File(...), photo_in: PhotoCreate = Depends(), db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)):

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


# GET /photos/{slug} - отримати фото за slug
@router.get("/{slug}", response_model=PhotoOut)
async def get_photo(slug: str, db: AsyncSession = Depends(get_db)):
    photo = crud_photo.get_photo_by_slug(db, slug)
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
    photo = await crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this photo")

    updated_photo = await crud_photo.update_photo(
        db=db,
        photo=photo,
        description=photo_in.description,
        tag_names=photo_in.tags
    )
    return updated_photo



# DELETE /photos/{id} - видалити фото
@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    photo = await crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this photo")

    cloudinary_service.delete_image(str(photo.cloudinary_public_id))
    await crud_photo.delete_photo(db, photo)
    return {"detail": "Photo deleted successfully"}


# POST /photos/{id}/transform - трансформація + QR
@router.post(
    "/{photo_id}/transform", # "/photos/{photo_id}/transform" ???????
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
    photo =await crud_photo.get_photo_by_id(db, photo_id)
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
        url=new_link.url, # type: ignore
        qr_code_url=new_link.qr_code_url, # type: ignore
        transformation_params=new_link.transformation_params # type: ignore
    )


# GET /photos/search - пошук і фільтрація
@router.get("/search", response_model=List[PhotoOut])
async def search_photos(
    keyword: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    photos = await crud_photo.search_photos(db, keyword=keyword, tag_name=tag)
    return photos



