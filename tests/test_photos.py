import io
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_upload_get_update_delete_photo(client, monkeypatch):
    # мокнемо функцію upload_image, повертає фіктивні дані
    monkeypatch.setattr("app.services.cloudinary_service.upload_image",
                        lambda f: {"public_id": "pid123", "url": "http://cloud/1.jpg"})

    # створимо користувача та отримаємо токен (реюзер або використовуємо fixture)
    signup = {"email": "bob@example.com", "password": "pass", "username": "bob"}
    r = await client.post("/api/users/signup", json=signup)
    assert r.status_code in (200,201)
    r = await client.post("/api/users/login", json={"email": "bob@example.com", "password": "pass"})
    tokens = r.json()
    access = tokens["access_token"]

    # upload (multipart/form-data)
    files = {"file": ("test.jpg", io.BytesIO(b"fake image bytes"), "image/jpeg")}
    data = {"description": "My photo", "tags": ["tag1", "tag2"]}
    headers = {"Authorization": f"Bearer {access}"}
    r = await client.post("/api/photos/upload", headers=headers, files=files, data={"photo_in": '{"description":"My photo","tags":["tag1","tag2"]}'})
    assert r.status_code == 200 or r.status_code == 201
    photo = r.json()
    photo_id = photo["id"]

    # get
    r = await client.get(f"/api/photos/{photo_id}")
    assert r.status_code == 200
    assert r.json()["description"] == "My photo"

    # update
    r = await client.put(f"/api/photos/{photo_id}", json={"description": "New desc", "tags": ["tag2"]}, headers=headers)
    assert r.status_code == 200
    assert r.json()["description"] == "New desc"

    # delete
    r = await client.delete(f"/api/photos/{photo_id}", headers=headers)
    assert r.status_code in (200, 204)
