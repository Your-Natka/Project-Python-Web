from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserCreate, UserLogin
from app.core.config import settings
from app.services.redis_service import add_to_blacklist
from uuid import uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_user(db: Session, user_in: UserCreate):
    user = User(
        email=user_in.email,
        username=user_in.username,
        password=pwd_context.hash(user_in.password),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = str(uuid4())
    to_encode.update({"exp": expire, "jti": jti})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def login_user(db: Session, user_in: UserLogin):
    user = authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise ValueError("Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


async def logout_user(jti: str):
    await add_to_blacklist(jti)
    return {"msg": "Successfully logged out"}

# --- 🔹 ДОДАНО: заглушки для відсутніх функцій --- #
async def refresh_token(token: str):
    # TODO: реалізувати перевипуск токену
    return {"msg": "Token refreshed (placeholder)"}


async def request_mail(email: str):
    # TODO: реалізувати надсилання пошти з підтвердженням
    return {"msg": f"Verification email sent to {email}"}


async def verify_mail(token: str):
    # TODO: реалізувати перевірку токена підтвердження пошти
    return {"msg": f"Email verified for token {token}"}



