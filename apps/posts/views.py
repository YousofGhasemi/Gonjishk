from django.db import IntegrityError, transaction
from likes.models import Like
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

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

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request: Request, pk: str | None = None) -> Response:
        post = self.get_object()
        try:
            with transaction.atomic():
                Like.objects.create(post=post, user=request.user)
        except IntegrityError:
            Like.objects.filter(post=post, user=request.user).delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)
        return Response({"liked": True}, status=status.HTTP_201_CREATED)
