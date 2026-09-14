from rest_framework import permissions, viewsets

from .models import Post
from .pagination import PostCursorPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = PostCursorPagination
    filterset_fields = ["author"]
    search_fields = ["content"]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)
