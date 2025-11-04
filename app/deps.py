# app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
import os
from app.models import User
from app.services.redis_service import is_blacklisted

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
        jti = payload.get("jti")
        if await is_blacklisted(jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")

        data = TokenData(
            user_id=payload.get("sub"),
            role=payload.get("role"),
            jti=jti
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return data

def require_role(min_role: str):
    roles = {"user": 1, "moderator": 2, "admin": 3}
    def role_dependency(current: TokenData = Depends(get_current_user)):
        if roles[current.role] < roles[min_role]:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current
    return role_dependency
