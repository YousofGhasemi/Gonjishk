import pytest
from comments.models import Comment
from posts.models import Post
from users.models import User


@pytest.mark.django_db
def test_create_comment_links_post_and_author() -> None:
    author = User.objects.create_user(
        username="author1",
        password="strong-pass-123",
    )
    commenter = User.objects.create_user(
        username="commenter1",
        password="strong-pass-123",
    )
    post = Post.objects.create(
        author=author,
        content="Hello, Gonjishk!",
    )

    comment = Comment.objects.create(
        post=post,
        author=commenter,
        content="Nice post!",
    )

    assert comment in post.comments.all()
    assert comment in commenter.comments.all()
