from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db.base import Base


class Role(PyEnum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), unique=True, nullable=False, index=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.user, nullable=False)
    bio = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)
    
    # relationships
    photos = relationship("Photo", back_populates="owner", cascade="all, delete")
    comments = relationship("Comment", back_populates="user", cascade="all, delete")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete")

    # def __repr__(self):
        # return f"<User(username={self.username}, role={self.role}, active={self.is_active})>"

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role}, active={self.is_active})>"

