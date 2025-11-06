from fastapi import APIRouter
from app.docs.descriptions import tags_description  # ✅ Імпортуємо описи

router = APIRouter(prefix="/api/tags", tags=["Tags"])

@router.get(
    "/",
    summary=tags_description["get_tags"]["summary"],
    description=tags_description["get_tags"]["description"]
)
async def get_tags():
    """
    Отримати список усіх тегів.
    """
    return {"message": "Tags list"}
