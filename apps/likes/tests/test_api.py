import pytest
from likes.models import Like
from posts.models import Post
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def author(db) -> User:
    return User.objects.create_user(username="author", password="strong-pass-123")


@pytest.fixture
def liker(db) -> User:
    return User.objects.create_user(username="liker", password="strong-pass-123")


@pytest.fixture
def post(author: User) -> Post:
    return Post.objects.create(author=author, content="Original post")


def _login(username: str) -> APIClient:
    client = APIClient()
    client.post("/api/v1/auth/login/", {"username": username, "password": "strong-pass-123"})
    return client


@pytest.mark.django_db
def test_liking_a_post_creates_like(post: Post, liker: User) -> None:
    client = _login("liker")

    response = client.post(f"/api/v1/posts/{post.id}/like/")

    assert response.status_code == 201
    assert response.data == {"liked": True}
    assert Like.objects.filter(post=post, user=liker).exists()


@pytest.mark.django_db
def test_liking_twice_toggles_to_unlike(post: Post, liker: User) -> None:
    client = _login("liker")

    client.post(f"/api/v1/posts/{post.id}/like/")
    response = client.post(f"/api/v1/posts/{post.id}/like/")

    assert response.status_code == 200
    assert response.data == {"liked": False}
    assert not Like.objects.filter(post=post, user=liker).exists()


@pytest.mark.django_db
def test_multiple_users_can_like_same_post(post: Post, author: User, liker: User) -> None:
    User.objects.create_user(username="liker2", password="strong-pass-123")

    _login("liker").post(f"/api/v1/posts/{post.id}/like/")
    _login("liker2").post(f"/api/v1/posts/{post.id}/like/")

    assert post.likes.count() == 2
