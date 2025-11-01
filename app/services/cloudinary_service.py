import cloudinary
import cloudinary.uploader
import cloudinary.utils
from app.core.config import settings
from typing import Dict, Optional

# Конфігурація Cloudinary
cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL, secure=True)


# upload_image(file) → URL + public_id
def upload_image(file) -> dict:
    """
    Завантажує файл на Cloudinary.
    Повертає dict з keys: 'url' та 'public_id'
    """
    result = cloudinary.uploader.upload(file)
    return {"url": result["secure_url"], "public_id": result["public_id"]}


# delete_image(public_id)
def delete_image(public_id: str):
    """
    Видаляє фото з Cloudinary
    """
    cloudinary.uploader.destroy(public_id)


#create_transformed_url(public_id, params)
def create_transformed_url(public_id: str, params: Optional[Dict] = None) -> str:
    """
    Створює URL для трансформованого зображення на Cloudinary
    params — словник з параметрами трансформації, наприклад:
        {"width": 300, "height": 300, "crop": "fill"}
    """
    params = params or {}
    url, options = cloudinary.utils.cloudinary_url(public_id, **params)
    return url
