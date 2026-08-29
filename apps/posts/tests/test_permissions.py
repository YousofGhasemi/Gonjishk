import pytest
from posts.models import Post
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def author(db) -> User:
    return User.objects.create_user(username="author", password="strong-pass-123")


@pytest.fixture
def other_user(db) -> User:
    return User.objects.create_user(username="other", password="strong-pass-123")


@pytest.fixture
def post(author: User) -> Post:
    return Post.objects.create(author=author, content="Original content")


def _login(client: APIClient, username: str) -> None:
    client.post(
        "/api/v1/auth/login/",
        {"username": username, "password": "strong-pass-123"},
    )


def test_non_author_cannot_update_post(post: Post, other_user: User) -> None:
    client = APIClient()
    _login(client, "other")

    response = client.patch(f"/api/v1/posts/{post.id}/", {"content": "Hacked!"})

    assert response.status_code == 403
    post.refresh_from_db()
    assert post.content == "Original content"


def test_author_can_update_own_post(post: Post, author: User) -> None:
    client = APIClient()
    _login(client, "author")

    response = client.patch(f"/api/v1/posts/{post.id}/", {"content": "Updated content"})

    assert response.status_code == 200
    post.refresh_from_db()
    assert post.content == "Updated content"
