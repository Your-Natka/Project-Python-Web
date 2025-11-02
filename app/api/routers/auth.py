from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/register")
async def register_user():
    return {"message": "User registered"}

@router.post("/token")
async def login_user():
    return {"access_token": "example_token"}

@router.post("/logout")
async def logout_user():
    return {"message": "User logged out"}