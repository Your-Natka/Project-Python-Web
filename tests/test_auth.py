import pytest

@pytest.mark.asyncio
async def test_signup_and_login(client):
    # --- Signup ---
    payload = {
        "email": "alice@example.com",
        "password": "password123",
        "username": "alice"
    }

    response = await client.post("/api/users/signup", json=payload)
    assert response.status_code in (200, 201), f"Unexpected signup status: {response.text}"

    data = response.json()
    assert data.get("email") == payload["email"]

    # --- Login ---
    response = await client.post("/api/users/login", json={
        "email": payload["email"],
        "password": payload["password"]
    })
    assert response.status_code == 200, f"Unexpected login status: {response.text}"

    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
