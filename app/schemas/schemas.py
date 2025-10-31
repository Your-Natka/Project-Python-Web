from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool

class Config:
        orm_mode = True


#COMMENTS

class CommentBase(BaseModel):
    """Базовая модель для комментариев."""
    content: str = Field(..., min_length=1, max_length=500, description="Текст Коментария")


class CommentCreate(CommentBase):
    """Модель для создания нового комментария."""
    photo_id: int = Field(..., description="ID фотографии, к которой добавляется комментарий")


class CommentUpdate(BaseModel):
    """Модель для обновления комментария."""
    content: str = Field(..., min_length=1, max_length=500, description="Обновлённый текст комментария")


class CommentInDBBase(CommentBase):
    """Базовая модель комментария из БД."""
    id: int
    user_id: int
    photo_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentResponse(CommentInDBBase):
    """Модель ответа для API."""
    username: str | None = None

#RATING

class RatingBase(BaseModel):
    """Базовая модель рейтинга."""
    value: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")


class RatingCreate(RatingBase):
    """Модель для создания нового рейтинга."""
    photo_id: int = Field(..., description="ID фотографии, которую оценивают")


class RatingUpdate(BaseModel):
    """Модель для обновления рейтинга."""
    value: int = Field(..., ge=1, le=5, description="Обновлённое значение рейтинга")


class RatingInDBBase(RatingBase):
    """Базовая модель рейтинга из БД."""
    id: int
    user_id: int
    photo_id: int

    class Config:
        orm_mode = True


class RatingResponse(RatingInDBBase):
    """Модель ответа для API рейтинга."""
    average_rating: float | None = None