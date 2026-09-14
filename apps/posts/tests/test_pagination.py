import pytest
from posts.models import Post
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def author(db) -> User:
    return User.objects.create_user(username="author", password="strong-pass-123")


@pytest.fixture
def authenticated_client(author: User) -> APIClient:
    client = APIClient()
    client.post(
        "/api/v1/auth/login/",
        {"username": "author", "password": "strong-pass-123"},
    )
    return client


@pytest.mark.django_db
def test_posts_list_is_paginated(authenticated_client: APIClient, author: User) -> None:
    for i in range(25):
        Post.objects.create(author=author, content=f"Post number {i}")

    response = authenticated_client.get("/api/v1/posts/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 20
    assert response.data["next"] is not None


@pytest.mark.django_db
def test_posts_search_filters_by_content(authenticated_client: APIClient, author: User) -> None:
    Post.objects.create(author=author, content="Learning Django architecture")
    Post.objects.create(author=author, content="Cooking pasta tonight")

    response = authenticated_client.get("/api/v1/posts/?search=Django")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert "Django" in response.data["results"][0]["content"]
