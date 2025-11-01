from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_ratings():
    return {"message": "List of ratings"}

@router.post("/")
async def create_rating():
    return {"message": "Rating created"}
