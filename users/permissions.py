from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Разрешение, которое проверяет, состоит ли пользователь в группе 'Moderators'.
    """
    def has_permission(self, request, view):
        # Если пользователь не авторизован, сразу отказываем
        if not request.user.is_authenticated:
            return False
        # Проверяем, есть ли пользователь в группе
        return request.user.groups.filter(name='Moderators').exists()

class IsOwner(BasePermission):
    """
    Разрешение, которое проверяет, является ли пользователь владельцем объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Проверяем, что у объекта есть поле owner и оно совпадает с текущим пользователем
        return hasattr(obj, 'owner') and obj.owner == request.user
