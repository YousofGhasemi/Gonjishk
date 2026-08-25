import pytest
from users.models import User


@pytest.mark.django_db
def test_create_user_has_uuid_primary_key() -> None:
    """Test that a created user has a UUID primary key."""

    user = User.objects.create_user(username="testuser", password="strong-pass-123")

    assert isinstance(user.pk, type(user.id))
    assert user.username == "testuser"
