from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.models.user import Role 
from app.models import User, Photo, Comment, Rating, Tag, TransformedLink

def main():
    db: Session = SessionLocal()

    admin_data = UserCreate(
        email="admin@example.com",
        password="supersecret",
        full_name="Admin Natka",
        role=Role.admin
    )

    create_user(db, admin_data)
    print("Admin created successfully!")

if __name__ == "__main__":
    main()
