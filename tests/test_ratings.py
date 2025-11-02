import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def async_client():
    """Создаёт тестового клиента для FastAPI"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_add_rating(async_client: AsyncClient):
    """
    Тест проверяет добавление нового рейтинга к фотографии.
    """
    response = await async_client.post(
        "/api/ratings/",
        json={"photo_id": 1, "value": 4}
    )

    assert response.status_code in (200, 201), f"Unexpected status: {response.status_code}"
    data = response.json()

    assert "photo_id" in data
    assert "value" in data
    assert data["value"] == 4


@pytest.mark.asyncio
async def test_rating_value_out_of_range(async_client: AsyncClient):
    """
    Тест проверяет, что нельзя поставить рейтинг вне диапазона 1–5.
    """
    response = await async_client.post(
        "/api/ratings/",
        json={"photo_id": 1, "value": 10}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_average_rating(async_client: AsyncClient):
    """
    Тест проверяет получение среднего рейтинга по фотографии.
    """
    await async_client.post("/api/ratings/", json={"photo_id": 2, "value": 5})
    await async_client.post("/api/ratings/", json={"photo_id": 2, "value": 3})

    response = await async_client.get("/api/ratings/photo/2")
    assert response.status_code == 200

    data = response.json()
    assert "average_rating" in data
    assert isinstance(data["average_rating"], (float, int)), "Ожидается числовое значение среднего рейтинга"