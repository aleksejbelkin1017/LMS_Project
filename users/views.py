from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт для получения и редактирования профиля пользователя.
    Доступен по ID пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
