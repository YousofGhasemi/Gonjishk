import pytest
from comments.models import Comment
from posts.models import Post
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def author(db) -> User:
    return User.objects.create_user(username="author", password="strong-pass-123")


@pytest.fixture
def commenter(db) -> User:
    return User.objects.create_user(username="commenter", password="strong-pass-123")


@pytest.fixture
def post(author: User) -> Post:
    return Post.objects.create(author=author, content="Original post")


def _login(username: str) -> APIClient:
    client = APIClient()
    client.post("/api/v1/auth/login/", {"username": username, "password": "strong-pass-123"})
    return client


@pytest.mark.django_db
def test_create_comment_on_post(post: Post, commenter: User) -> None:
    client = _login("commenter")

    response = client.post(f"/api/v1/posts/{post.id}/comments/", {"content": "Nice post!"})

    assert response.status_code == 201
    assert Comment.objects.filter(post=post, author=commenter, content="Nice post!").exists()


@pytest.mark.django_db
def test_comments_list_only_shows_comments_for_that_post(
    post: Post, author: User, commenter: User
) -> None:
    other_post = Post.objects.create(author=author, content="Another post")
    Comment.objects.create(post=post, author=commenter, content="On first post")
    Comment.objects.create(post=other_post, author=commenter, content="On second post")

    client = _login("commenter")
    response = client.get(f"/api/v1/posts/{post.id}/comments/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["content"] == "On first post"


@pytest.mark.django_db
def test_non_author_cannot_delete_comment(post: Post, author: User, commenter: User) -> None:
    comment = Comment.objects.create(post=post, author=commenter, content="Nice post!")
    client = _login("author")

    response = client.delete(f"/api/v1/posts/{post.id}/comments/{comment.id}/")

    assert response.status_code == 403
    assert Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_creating_comment_on_nonexistent_post_returns_404(commenter: User) -> None:
    client = _login("commenter")
    fake_post_id = "00000000-0000-0000-0000-000000000000"

    response = client.post(f"/api/v1/posts/{fake_post_id}/comments/", {"content": "Nice post!"})

    assert response.status_code == 404
