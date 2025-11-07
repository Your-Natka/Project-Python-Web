from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import auth_service
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача.
    Перший користувач отримує роль 'admin'.
    """
    return await auth_service.register_user(db, user_data)


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Логін користувача. Повертає JWT токен.
    """
    return await auth_service.login_user(db, login_data)


@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Підтвердження email користувача за токеном.
    """
    return await auth_service.verify_mail(db, token)
