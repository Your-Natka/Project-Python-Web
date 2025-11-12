# from datetime import datetime
# from typing import Optional
# from pydantic import BaseModel, EmailStr
# from enum import Enum


# class Role(str, Enum):
#     user = "user"
#     moderator = "moderator"
#     admin = "admin"


# # --- Базова схема ---
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None
#     bio: Optional[str] = None
#     avatar_url: Optional[str] = None


# # --- Для створення нового користувача ---
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
#     username: str
#     full_name: str
#     bio: Optional[str] = None
#     avatar_url: Optional[str] = None
#     role: Optional[Role] = Role.user 


# # --- Для оновлення профілю користувача ---
# class UserUpdate(BaseModel):
#     full_name: Optional[str] = None
#     bio: Optional[str] = None
#     avatar_url: Optional[str] = None


# # --- Для відповіді API (повертається користувач) ---
# class UserResponse(UserBase):
#     id: int
#     role: Role
#     is_active: bool
#     registered_at: datetime

#     class Config:
#         from_attributes = True


# # --- Для логіну / токена ---
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


# # --- Для токена відповіді ---
# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
