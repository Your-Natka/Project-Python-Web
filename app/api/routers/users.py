from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.docs.descriptions import users_description  # ✅ додано
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    create_user, login_user, refresh_token, request_mail, verify_mail, logout_user
)
from app.deps import require_role
from app.db.session import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "/signup",
    response_model=UserResponse,
    summary=users_description["signup"]["summary"],
    description=users_description["signup"]["description"]
)
async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Реєстрація нового користувача"""
    return create_user(db, user_in)


@router.post(
    "/login",
    summary=users_description["login"]["summary"],
    description=users_description["login"]["description"]
)
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Авторизація користувача"""
    return login_user(db, user_in)

@router.post(
    "/refresh_token",
    summary=users_description["refresh_token"]["summary"],
    description=users_description["refresh_token"]["description"]
)
async def refresh(token: str):
    """Оновлення access токена"""
    return await refresh_token(token)


@router.post(
    "/request_mail",
    summary=users_description["request_mail"]["summary"],
    description=users_description["request_mail"]["description"]
)
async def send_mail_request(email: str):
    """Надіслати лист для верифікації"""
    return await request_mail(email)


@router.get(
    "/request_mail/{token}",
    summary=users_description["confirm_mail"]["summary"],
    description=users_description["confirm_mail"]["description"]
)
async def confirm_mail(token: str):
    """Підтвердити email через токен"""
    return await verify_mail(token)


@router.get(
    "/admin",
    dependencies=[Depends(require_role("admin"))],
    summary=users_description["admin"]["summary"],
    description=users_description["admin"]["description"]
)
async def get_admins():
    """Доступ лише для адміністраторів"""
    return {"message": "Admin access granted"}


@router.get(
    "/moderator",
    dependencies=[Depends(require_role("moderator"))],
    summary=users_description["moderator"]["summary"],
    description=users_description["moderator"]["description"]
)
async def get_moderators():
    """Доступ лише для модераторів"""
    return {"message": "Moderator access granted"}


@router.post(
    "/logout",
    summary=users_description["logout"]["summary"],
    description=users_description["logout"]["description"]
)
async def logout(jti: str):
    """Вихід користувача (деактивація токена)"""
    return await logout_user(jti)
