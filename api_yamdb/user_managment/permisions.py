from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class IsOwnerIReadOnly(permissions.BasePermission):
    """Имеет право распоряжаться своим контентом"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
    

class IsModerator(permissions.BasePermission):
    """Модератор может удалять и редактировать любые отзывы и комментарии"""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == MODERATOR
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
    
class IsAdmin(permissions.BasePermission):
    """Полная свобода действий"""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == ADMIN
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор может все, остальные только читать."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == ADMIN
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (
                request.user.role == ADMIN 
                or request.user.is_superuser
            ))
        )