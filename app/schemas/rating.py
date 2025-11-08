from pydantic import BaseModel, Field
from datetime import datetime

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
