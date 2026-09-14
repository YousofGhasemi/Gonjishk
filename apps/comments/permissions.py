from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Comment


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Comment) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
