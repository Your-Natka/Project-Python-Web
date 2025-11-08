from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.config import settings
from app.utils.mailer import send_verification_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7
        self.blacklist = set()

    # ==========================================================
    # 1️⃣ Реєстрація користувача
    # ==========================================================
    async def register_user(self, db: Session, user_in: UserCreate):
        existing = db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Користувач з таким email вже існує")

        # перший користувач у системі → admin
        count_users = db.query(User).count()
        role = "admin" if count_users == 0 else "user"

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

        token = self._create_email_token(user.email)
        await send_verification_email(user.email, token)

        return UserResponse.from_orm(user)

    # ==========================================================
    # 2️⃣ Логін користувача
    # ==========================================================
    async def login_user(self, db: Session, user_in: UserLogin):
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user or not pwd_context.verify(user_in.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Невірний email або пароль")

        access_token = self._create_access_token({"sub": user.email})
        refresh_token = self._create_refresh_token({"sub": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    # ==========================================================
    # 3️⃣ Оновлення токена
    # ==========================================================
    async def refresh_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Недійсний refresh токен")

        new_access_token = self._create_access_token({"sub": email})
        return {"access_token": new_access_token, "token_type": "bearer"}

    # ==========================================================
    # 4️⃣ Підтвердження email
    # ==========================================================
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
        return {"message": "Email успішно підтверджено"}

    # ==========================================================
    # 5️⃣ Вихід користувача (logout)
    # ==========================================================
    async def logout_user(self, jti: str):
        self.blacklist.add(jti)
        return {"message": "Користувача успішно вийшов з системи"}

    # ==========================================================
    # 🔒 Приватні допоміжні методи
    # ==========================================================
    def _create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "jti": str(uuid4())})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def _create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "jti": str(uuid4())})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def _create_email_token(self, email: str):
        expire = datetime.utcnow() + timedelta(hours=24)
        data = {"sub": email, "exp": expire}
        return jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)


auth_service = AuthService()
