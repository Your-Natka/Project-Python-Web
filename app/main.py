from fastapi import FastAPI
from app.api.routers import users, auth, photos, tags, comments, ratings
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api import search 

# Створюємо всі таблиці (для dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhotoShare API")

@app.get("/")
def read_root():
    return {"message": "Hello, PhotoShare API!"}

# 🔗 Підключення роутерів
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(photos.router, prefix="/photos", tags=["Photos"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
app.include_router(search.router)

