from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.schemas import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()
