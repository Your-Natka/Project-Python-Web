import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_comment(async_client: AsyncClient):
    """Перевіряємо створення нового коментаря"""
    response = await async_client.post(
        "/api/comments/",
        json={"photo_id": 1, "text": "Класне фото!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Класне фото!"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_update_comment(async_client: AsyncClient):
    """Перевіряємо оновлення коментаря"""
    response = await async_client.put(
        "/api/comments/1",
        json={"text": "Оновлений коментар"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Оновлений коментар"


@pytest.mark.asyncio
async def test_admin_can_delete_comment(async_client: AsyncClient):
    """Адмін може видаляти коментарі"""
    response = await async_client.delete("/api/comments/1")
    assert response.status_code in (200, 204)