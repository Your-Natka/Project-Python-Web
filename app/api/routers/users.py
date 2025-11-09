from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.docs.descriptions import users_description
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.deps import require_role, get_current_user, oauth2_scheme
from app.db.session import get_db
from app.services.auth_service import AuthService 
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm


auth_service = AuthService()

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)


@router.post(
    "/signup",
    response_model=UserResponse,
    summary=users_description["signup"]["summary"],
    description=users_description["signup"]["description"]
)
async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Реєстрація нового користувача"""
    return await auth_service.register_user(db=db, user_in=user_in)


@router.post(
    "/login",
    summary=users_description["login"]["summary"],
    description=users_description["login"]["description"]
)
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Авторизація користувача"""
    return await auth_service.login_user(db=db, user_in=user_in)


@router.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Swagger UI робить POST сюди через form-data (email + password)
    Тепер response_model=Token
    """
    user_in = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.login_user(db=db, user_in=user_in)


@router.post(
    "/refresh_token",
    summary=users_description["refresh_token"]["summary"],
    description=users_description["refresh_token"]["description"]
)
# async def refresh(token: str):
#     """Оновлення access токена"""
#     return await auth_service.refresh_token(token)
async def refresh(authorization: str = Header(..., description="Bearer token")):
    token = authorization.split(" ")[1]
    return await auth_service.refresh_token(token)

@router.post(
    "/request_mail",
    summary=users_description["request_mail"]["summary"],
    description=users_description["request_mail"]["description"]
)
async def send_mail_request(email: str):
    """Надіслати лист для верифікації"""
    return await auth_service.request_mail(email)


@router.get(
    "/request_mail/{token}",
    summary=users_description["confirm_mail"]["summary"],
    description=users_description["confirm_mail"]["description"]
)
# async def confirm_mail(token: str):
#     """Підтвердити email через токен"""
#     return await auth_service.verify_mail(db, token)
async def confirm_mail(token: str, db: Session = Depends(get_db)):
    return await auth_service.verify_mail(db, token)



@router.get(
    "/admin",
    dependencies=[Depends(require_role("admin"))],
    summary=users_description["admin"]["summary"],
    description=users_description["admin"]["description"]
)
# async def get_admins():
#     """Доступ лише для адміністраторів"""
#     return {"message": "Admin access granted"}
async def get_admins(current_user: User = Depends(get_current_user)):  # додаємо Depends
    """Доступ лише для адміністраторів"""
    return {"message": f"Admin access granted for {current_user.email}"}

@router.get(
    "/moderator",
    dependencies=[Depends(require_role("moderator"))],
    summary=users_description["moderator"]["summary"],
    description=users_description["moderator"]["description"]
)
# async def get_moderators():
#     """Доступ лише для модераторів"""
#     return {"message": "Moderator access granted"}
async def get_moderators(current_user: User = Depends(get_current_user)):  # додаємо Depends
    """Доступ лише для модераторів"""
    return {"message": f"Moderator access granted for {current_user.email}"}


@router.post(
    "/logout",
    summary=users_description["logout"]["summary"],
    description=users_description["logout"]["description"]
)
# async def logout(authorization: str = Header(...)):
#     """Вихід користувача (деактивація токена)"""
#     token = authorization.split(" ")[1]  # Bearer <token>
#     return await auth_service.logout_user(token)
async def logout(authorization: str = Header(..., description="Bearer token")):
    """Вихід користувача (деактивація токена)"""
    token = authorization.split(" ")[1]  # Bearer <token>
    return await auth_service.logout_user(token)
