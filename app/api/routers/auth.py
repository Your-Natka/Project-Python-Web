from fastapi import APIRouter, Depends, status
from app.deps import get_current_user
from app.services.redis_service import add_to_blacklist
from app.docs.descriptions import auth_description  # ✅ додаємо імпорт опису

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/logout",
    summary=auth_description["logout"]["summary"],
    description=auth_description["logout"]["description"],
    status_code=status.HTTP_200_OK
)
async def logout(current_user=Depends(get_current_user)):
    """
    Завершення сеансу користувача.  
    Додає поточний JWT токен у чорний список Redis.
    """
    await add_to_blacklist(current_user.jti)
    return {"detail": "Successfully logged out"}
