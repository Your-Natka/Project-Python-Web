from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_comment():
    return {"message": "Comment created"}

@router.get("/")
async def get_comments():
    return {"message": "List of comments"}