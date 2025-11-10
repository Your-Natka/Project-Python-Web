from datetime import datetime, timedelta
from uuid import uuid4
import logging

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import redis.asyncio as redis

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.config import settings
from app.utils.mailer import send_verification_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger("auth")


class AuthService:
    def __init__(self):
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7
        self.EMAIL_TOKEN_EXPIRE_HOURS = 24

        # Redis для blacklist
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    # ==================== РЕЄСТРАЦІЯ ====================
    async def register_user(self, db: Session, user_in: UserCreate):
        if db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first():
            raise HTTPException(status_code=400, detail="Email або username вже використовується")

        role = "admin" if db.query(User).count() == 0 else "user"
        hashed_password = pwd_context.hash(user_in.password)
        user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            bio=user_in.bio,
            avatar_url=user_in.avatar_url,
            hashed_password=hashed_password,
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = self._create_token(user.email, self.EMAIL_TOKEN_EXPIRE_HOURS, token_type="email")
        await send_verification_email(user.email, token)
        logger.info(f"New user registered: {user.email}")

        return UserResponse.from_orm(user)

    # ==================== ЛОГІН ====================
    async def login_user(self, db: Session, user_in: UserLogin):
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user or not pwd_context.verify(user_in.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Невірний email або пароль")

        if not user.is_verified:
            raise HTTPException(status_code=403, detail="Email не підтверджено")

        access_token = self._create_token(user.email, self.ACCESS_TOKEN_EXPIRE_MINUTES, "access")
        refresh_token = self._create_token(user.email, self.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60, "refresh")
        logger.info(f"User logged in: {user.email}")

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    # ==================== ОНОВЛЕННЯ ТОКЕНА ====================
    async def refresh_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload.get("sub")
            jti = payload.get("jti")
            if await self.redis.get(f"blacklist:{jti}"):
                raise HTTPException(status_code=401, detail="Токен недійсний")
        except JWTError:
            raise HTTPException(status_code=401, detail="Недійсний refresh токен")

        new_access_token = self._create_token(email, self.ACCESS_TOKEN_EXPIRE_MINUTES, "access")
        logger.info(f"Access token refreshed for: {email}")
        return {"access_token": new_access_token, "token_type": "bearer"}

    # ==================== ПІДТВЕРДЖЕННЯ EMAIL ====================
    async def verify_mail(self, db: Session, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=400, detail="Недійсний або прострочений токен")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")

        user.is_verified = True
        db.commit()
        logger.info(f"Email verified for: {email}")
        return {"message": "Email успішно підтверджено"}

    # ==================== LOGOUT ====================
    async def logout_user(self, jti: str, expire_seconds: int):
        await self.redis.set(f"blacklist:{jti}", "true", ex=expire_seconds)
        logger.info(f"Token blacklisted: {jti}")
        return {"message": "Користувача успішно вийшов з системи"}

    # ==================== ПРИВАТНИЙ МЕТОД ДЛЯ ТОКЕНІВ ====================
    def _create_token(self, email: str, expire_minutes: int, token_type: str):
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        payload = {"sub": email, "exp": expire, "jti": str(uuid4()), "type": token_type}
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)


auth_service = AuthService()
