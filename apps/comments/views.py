from django.shortcuts import get_object_or_404
from posts.models import Post
from rest_framework import permissions, viewsets

from .models import Comment
from .pagination import CommentCursorPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = CommentCursorPagination

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"])

    def perform_create(self, serializer) -> None:
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(author=self.request.user, post=post)
