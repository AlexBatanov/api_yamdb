from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """Проверка наличия прав у пользователя на изменение/удаление контента."""
    message = 'Изменение или удаление чужого контента запрещено!.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
