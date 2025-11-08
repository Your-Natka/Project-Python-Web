import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.photo import Photo
from app.models.transformed_link import TransformedLink

client = TestClient(app)


@pytest.fixture
def mock_current_user():
    return {"user_id": 1, "role": "user"}


@pytest.fixture
def sample_photo():
    return Photo(
        id=1,
        owner_id=1,
        cloudinary_public_id="test_public_id",
        cloudinary_url="https://example.com/image.jpg",
        description="Test photo",
        unique_slug="test-photo"
    )



# Завантаження фото
@patch("app.services.cloudinary_service.upload_image")
@patch("app.api.routers.photos.get_current_user")
def test_upload_photo(mock_user, mock_upload):
    mock_user.return_value = {"user_id": 1}
    mock_upload.return_value = {"public_id": "abc123", "url": "https://cdn.example.com/test.jpg"}

    files = {"file": ("test.jpg", b"fakeimagebytes", "image/jpeg")}
    data = {"description": "A test image", "tags": ["test", "photo"]}

    response = client.post("/photos/", files=files, data=data)

    assert response.status_code == 200
    body = response.json()
    assert "cloudinary_url" in body
    assert body["description"] == "A test image"


# Отримання фото за slug
@patch("app.api.routers.photos.get_db")
def test_get_photo(mock_db, sample_photo):
    class MockResult:
        def scalars(self):
            return self
        def first(self):
            return sample_photo

    mock_db.return_value.__aenter__.return_value.execute.return_value = MockResult()

    response = client.get("/photos/test-photo")

    assert response.status_code == 200
    data = response.json()
    assert data["unique_slug"] == "test-photo"


# Оновлення фото
@patch("app.api.routers.photos.get_current_user")
@patch("app.api.routers.photos.get_db")
def test_update_photo(mock_db, mock_user, sample_photo):
    mock_user.return_value = {"user_id": 1}

    class MockResult:
        def scalars(self):
            return self
        def first(self):
            return sample_photo

    mock_db.return_value.__aenter__.return_value.execute.return_value = MockResult()

    response = client.put(
        "/photos/1",
        json={"description": "Updated description", "tags": ["newtag"]}
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"


#  Видалення фото
@patch("app.api.routers.photos.get_current_user")
@patch("app.api.routers.photos.cloudinary_service.delete_image")
@patch("app.api.routers.photos.get_db")
def test_delete_photo(mock_db, mock_delete, mock_user, sample_photo):
    mock_user.return_value = {"user_id": 1}
    mock_delete.return_value = None

    class MockResult:
        def scalars(self):
            return self
        def first(self):
            return sample_photo

    mock_db.return_value.__aenter__.return_value.execute.return_value = MockResult()

    response = client.delete("/photos/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Photo deleted successfully"



#  Трансформація фото (Cloudinary + QR)
@patch("app.services.qr_services.generate_qr_code")
@patch("app.services.cloudinary_service.create_transformed_url")
@patch("app.api.routers.photos.require_role")
@patch("app.api.routers.photos.get_db")
def test_transform_photo(mock_db, mock_role, mock_transform, mock_qr, sample_photo):
    mock_role.return_value = lambda: {"user_id": 1}
    mock_transform.return_value = "https://cdn.example.com/transformed.jpg"
    mock_qr.return_value = "https://cdn.example.com/qr.png"

    class MockResult:
        def scalars(self):
            return self
        def first(self):
            return sample_photo
        def scalar_one_or_none(self):
            return sample_photo

    mock_db.return_value.__aenter__.return_value.execute.return_value = MockResult()

    response = client.post("/photos/1/transform?width=200&height=200")

    assert response.status_code == 201
    data = response.json()
    assert "url" in data
    assert "qr_code_url" in data


#  Пошук фото
@patch("app.api.routers.photos.get_db")
def test_search_photos(mock_db, sample_photo):
    class MockResult:
        def scalars(self):
            return self
        def all(self):
            return [sample_photo]

    mock_db.return_value.__aenter__.return_value.execute.return_value = MockResult()

    response = client.get("/photos/search?keyword=test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["unique_slug"] == "test-photo"
 
