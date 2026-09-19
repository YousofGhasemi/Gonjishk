import uuid

from django.conf import settings
from django.db import models
from posts.models import Post


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_post_like_per_user")
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user} likes {self.post_id}"
