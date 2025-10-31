from fastapi import FastAPI
from app.api.routers import users
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# Створюємо всі таблиці (для dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My FastAPI Project")

# Регіструємо роутери
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
