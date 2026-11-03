from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт для получения и редактирования профиля пользователя.
    Доступен по ID пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    """
    Эндпоинт для вывода списка платежей.
    Поддерживает фильтрацию и сортировку.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Настраиваем фильтры: DjangoFilterBackend для точной фильтрации и OrderingFilter для сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Поля для фильтрации (Задание 4): по курсу, по уроку, по способу оплаты
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']

    # Поля для сортировки (Задание 4): по дате оплаты
    ordering_fields = ['payment_date']