from fastapi import APIRouter, Depends, status
from app.deps import get_current_user
from app.services.redis_service import add_to_blacklist

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user=Depends(get_current_user)):
    # Додати JTI токена в Redis blacklist
    await add_to_blacklist(current_user.jti)
    return {"detail": "Successfully logged out"}