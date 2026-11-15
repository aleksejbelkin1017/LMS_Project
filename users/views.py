from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lms.models import Course
from users.services import create_stripe_product, create_stripe_price, create_stripe_session
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


class PaymentCreateAPIView(APIView):
    """Эндпоинт для создания платежа и получения ссылки на оплату."""

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        amount = request.data.get('amount')  # Сумма в рублях

        if not course_id or not amount:
            return Response(
                {"error": "Не переданы course_id или amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        try:
            # 1. Создаем продукт в Stripe
            product_id = create_stripe_product(course.name)

            # 2. Создаем цену в Stripe
            price_id = create_stripe_price(product_id, int(amount))

            # 3. Создаем сессию для оплаты
            session_data = create_stripe_session(price_id)

            # 4. Сохраняем все данные в нашу модель Payment
            payment = Payment.objects.create(
                user=request.user,
                paid_course=course,
                amount=amount,
                payment_method=Payment.PAYMENT_METHOD_TRANSFER,
                stripe_product_id=product_id,
                stripe_price_id=price_id,
                stripe_session_id=session_data['session_id'],
                payment_url=session_data['url']
            )

            # 5. Возвращаем данные о платеже
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)