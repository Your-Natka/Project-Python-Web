from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_tags():
    return {"message": "List of tags"}