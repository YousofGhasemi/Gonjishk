import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
def test_register_creates_user_with_hashed_password() -> None:
    client = APIClient()
    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "S3cure!Pass123",
            "password_confirm": "S3cure!Pass123",
        },
    )

    assert response.status_code == 201
    user = User.objects.get(username="newuser")
    assert user.check_password("S3cure!Pass123")
    assert "password" not in response.data


@pytest.mark.django_db
def test_register_fails_when_passwords_do_not_match() -> None:
    client = APIClient()
    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "S3cure!Pass123",
            "password_confirm": "DifferentPass456",
        },
    )

    assert response.status_code == 400
    assert not User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_fails_with_weak_password() -> None:
    client = APIClient()
    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "12345",
            "password_confirm": "12345",
        },
    )

    assert response.status_code == 400
    assert not User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_fails_with_duplicate_username() -> None:
    User.objects.create_user(username="existing", password="S3cure!Pass123")
    client = APIClient()

    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "existing",
            "email": "another@example.com",
            "password": "S3cure!Pass123",
            "password_confirm": "S3cure!Pass123",
        },
    )

    assert response.status_code == 400
