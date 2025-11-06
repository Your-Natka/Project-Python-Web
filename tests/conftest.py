import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db


# 🧩 SQLite in-memory (швидкий тестовий варіант)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 🔧 створення/видалення таблиць один раз за сесію
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# 🧩 Сесія БД для кожного тесту
@pytest_asyncio.fixture()
async def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# 🧪 Клієнт для HTTP-запитів із заміненим get_db
@pytest_asyncio.fixture()
async def client(db_session, monkeypatch):
    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    # заміна залежності FastAPI
    monkeypatch.setattr("app.db.session.get_db", _get_test_db)

    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c
