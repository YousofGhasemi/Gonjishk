from posts.urls import router as posts_router
from rest_framework_nested import routers

from .views import CommentViewSet

comments_router = routers.NestedDefaultRouter(posts_router, "posts", lookup="post")
comments_router.register("comments", CommentViewSet, basename="post-comments")

urlpatterns = comments_router.urls
