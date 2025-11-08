from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    create_user, login_user, refresh_token, request_mail, verify_mail, logout_user
)
from app.deps import require_role, get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/signup", response_model=UserResponse)
async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)


@router.post("/login")
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_in)


@router.post("/refresh_token")
async def refresh(token: str):
    return await refresh_token(token)


@router.post("/request_mail")
async def send_mail_request(email: str):
    return await request_mail(email)


@router.get("/request_mail/{token}")
async def confirm_mail(token: str):
    return await verify_mail(token)


@router.get("/admin", dependencies=[Depends(require_role("admin"))])
async def get_admins():
    return {"message": "Admin access granted"}


@router.get("/moderator", dependencies=[Depends(require_role("moderator"))])
async def get_moderators():
    return {"message": "Moderator access granted"}


@router.post("/logout")
async def logout(jti: str):
    return await logout_user(jti)
