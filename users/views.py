from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    UserPublicSerializer,
    PaymentSerializer,
    UserRegisterSerializer
)
from users.permissions import IsSelfOrReadOnly


class UserListCreateAPIView(generics.ListCreateAPIView):
    """Список пользователей и регистрация."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        return UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление пользователя с разными правами."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get_serializer_class(self):
        # Если пользователь смотрит свой профиль — показываем полный
        if self.request.user == self.get_object():
            return UserSerializer
        # Если чужой — только публичные данные
        return UserPublicSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Эндпоинт для вывода списка платежей с фильтрацией и сортировкой."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
