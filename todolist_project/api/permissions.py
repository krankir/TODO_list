from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrAuthor(BasePermission):
    """Разрешение для администратора или автора"""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
