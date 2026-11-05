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
