from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# ---------------- USERS ----------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

# ---------------- COMMENTS ----------------
class CommentBase(BaseModel):
    """Базова модель для коментарів."""
    content: str = Field(..., min_length=1, max_length=500, description="Текст коментаря")

class CommentCreate(CommentBase):
    """Модель для створення нового коментаря."""
    photo_id: int = Field(..., description="ID фотографії, до якої додається коментар")

class CommentUpdate(BaseModel):
    """Модель для оновлення коментаря."""
    content: str = Field(..., min_length=1, max_length=500, description="Оновлений текст коментаря")

class CommentInDBBase(CommentBase):
    """Базова модель коментаря з БД."""
    id: int
    user_id: int
    photo_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentResponse(CommentInDBBase):
    """Модель відповіді для API."""
    username: str | None = None

# ---------------- RATINGS ----------------
class RatingBase(BaseModel):
    """Базова модель рейтингу."""
    value: int = Field(..., ge=1, le=5, description="Оцінка від 1 до 5")

class RatingCreate(RatingBase):
    """Модель для створення нового рейтингу."""
    photo_id: int = Field(..., description="ID фотографії, яку оцінюють")

class RatingUpdate(BaseModel):
    """Модель для оновлення рейтингу."""
    value: int = Field(..., ge=1, le=5, description="Оновлене значення рейтингу")

class RatingInDBBase(RatingBase):
    """Базова модель рейтингу з БД."""
    id: int
    user_id: int
    photo_id: int

    class Config:
        from_attributes = True

class RatingResponse(RatingInDBBase):
    """Модель відповіді для API рейтингу."""
    average_rating: float | None = None
