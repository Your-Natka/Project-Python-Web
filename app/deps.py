from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2, OAuth2PasswordBearer
from app.core.config import settings
from app.models.user import User, Role
from app.db.session import get_db
from sqlalchemy.orm import Session



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_role(required_role: Role):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != Role.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation allowed only for role: {required_role}",
            )
        return current_user
    return role_checker
