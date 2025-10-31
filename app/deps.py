# app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

class TokenData(BaseModel):
    user_id: str
    role: str
    jti: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenData(
            user_id=payload.get("sub"),
            role=payload.get("role"),
            jti=payload.get("jti")
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # TODO: check in DB user exists and is_active
    # TODO: check jti not in blacklist (Redis)
    return data

def require_role(min_role: str):
    roles = {"user": 1, "moderator": 2, "admin": 3}
    def role_dependency(current: TokenData = Depends(get_current_user)):
        if roles[current.role] < roles[min_role]:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current
    return role_dependency
