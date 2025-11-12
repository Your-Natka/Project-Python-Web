# from fastapi import FastAPI
# from app.api.routers import users, auth, photos, tags, comments, ratings
# from app.core.config import settings
# from app.db.session import engine
# from app.db.base import Base
# from app.api.routers import search 
# from fastapi.security import OAuth2PasswordBearer
# from fastapi.middleware.cors import CORSMiddleware

# # Створюємо всі таблиці (для dev)
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="PhotoShare API")
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # або ["http://localhost:3000"] для безпеки
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # 🔗 Підключення роутерів
# # app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# # app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(users.router)
# app.include_router(photos.router, prefix="/photos", tags=["Photos"])
# app.include_router(tags.router, prefix="/tags", tags=["Tags"])
# app.include_router(comments.router, prefix="/comments", tags=["Comments"])
# app.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
# app.include_router(search.router)

# @app.get("/")
# def read_root():
#     return {"message": "Hello, PhotoShare API!"}

