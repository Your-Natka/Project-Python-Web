import os
import qrcode
from io import BytesIO
from typing import Optional
from app.services import cloudinary_service
import qrcode
from qrcode.constants import ERROR_CORRECT_H


# Папка для локального збереження QR-кодів
LOCAL_QR_DIR = "media/qrcodes"
os.makedirs(LOCAL_QR_DIR, exist_ok=True)


# Генерація QR-кодів.
def generate_qr_code(data: str, save_to: Optional[str] = None, filename: Optional[str] = None) -> str:
    """
    Генерує QR-код для переданого data (зазвичай URL)

    Параметри:
        data: str — текст чи URL, який кодується
        save_to: Optional[str] — "local", "cloudinary" чи None
        filename: Optional[str] — ім'я файлу (без шляху), якщо зберігаємо локально
    
    Повертає:
        - Якщо save_to="local": шлях до PNG файлу
        - Якщо save_to="cloudinary": URL на Cloudinary
        - Якщо save_to=None: base64-encoded string
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,  
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    if save_to == "local":
        # Якщо ім'я файлу не вказано, генеруємо випадкове
        if not filename:
            import uuid
            filename = f"{uuid.uuid4().hex}.png"
        path = os.path.join(LOCAL_QR_DIR, filename)
        img.save(path) # type: ignore
        return path

    elif save_to == "cloudinary":
        # Зберігаємо в пам'ять
        buffer = BytesIO()
        img.save(buffer, format="PNG") # type: ignore
        buffer.seek(0)
        # Використовуємо cloudinary_service для завантаження
        result = cloudinary_service.upload_image(buffer)
        return result["url"]

    else:
        # Повертаємо base64 string
        buffer = BytesIO()
        img.save(buffer, format="PNG") # type: ignore
        buffer.seek(0)
        import base64
        img_bytes = buffer.getvalue()
        base64_str = base64.b64encode(img_bytes).decode("utf-8")
        return f"data:image/png;base64,{base64_str}"
