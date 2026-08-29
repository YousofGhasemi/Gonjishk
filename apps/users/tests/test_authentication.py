import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(username="tester", password="strong-pass-123")


def test_login_sets_httponly_cookies(user: User) -> None:
    client = APIClient()
    response = client.post(
        "/api/v1/auth/login/",
        {"username": "tester", "password": "strong-pass-123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert response.cookies["access_token"]["httponly"] is True


def test_posts_endpoint_requires_authentication() -> None:
    client = APIClient()
    response = client.get("/api/v1/posts/")

    assert response.status_code == 401


def test_login_then_access_protected_endpoint(user: User) -> None:
    client = APIClient()
    client.post(
        "/api/v1/auth/login/",
        {"username": "tester", "password": "strong-pass-123"},
    )

    response = client.get("/api/v1/posts/")

    assert response.status_code == 200
