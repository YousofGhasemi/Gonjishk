import pytest
from posts.models import Post
from users.models import User


@pytest.mark.django_db
def test_create_post_sets_author_and_uuid_pk() -> None:
    user = User.objects.create_user(username="author1", password="strong-pass-123")
    post = Post.objects.create(author=user, content="Hello, Gonjishk!")

    assert isinstance(post.pk, type(post.id))
    assert post.author == user
    assert post in user.posts.all()
