# from pydantic import BaseModel, Field
# from datetime import datetime

# class CommentBase(BaseModel):
#     """Базова модель для коментарів."""
#     content: str = Field(..., min_length=1, max_length=500, description="Текст коментаря")

# class CommentCreate(CommentBase):
#     """Модель для створення нового коментаря."""
#     photo_id: int = Field(..., description="ID фотографії, до якої додається коментар")

# class CommentUpdate(BaseModel):
#     """Модель для оновлення коментаря."""
#     content: str = Field(..., min_length=1, max_length=500, description="Оновлений текст коментаря")

# class CommentInDBBase(CommentBase):
#     """Базова модель коментаря з БД."""
#     id: int
#     user_id: int
#     photo_id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True

# class CommentResponse(CommentInDBBase):
#     """Модель відповіді для API."""
#     username: str | None = None
