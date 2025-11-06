import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_search_photos(client: AsyncClient):
    # Виконуємо пошук фото за ключовим словом
    response = await client.get("/search", params={"query": "nature"})

    # Перевіряємо статус-код
    assert response.status_code == 200

    data = response.json()

    # Перевіряємо, що результат має правильну структуру
    assert "results" in data
    assert isinstance(data["results"], list)

    # Якщо є результати — перевіряємо, що у фото є очікувані ключі
    if data["results"]:
        photo = data["results"][0]
        assert "id" in photo
        assert "url" in photo
        assert "tags" in photo
