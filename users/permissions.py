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

class IsSelfOrReadOnly(BasePermission):
    """
    Разрешение: читать может любой авторизованный,
    а изменять — только владелец профиля.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Изменять (PUT, PATCH, DELETE) можно только свой профиль
        return obj == request.user
