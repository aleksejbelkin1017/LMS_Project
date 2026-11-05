from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserRetrieveUpdateAPIView, PaymentListAPIView

urlpatterns = [
    # Эндпоинты для JWT-авторизации (доступны всем)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Эндпоинты пользователей
    path('users/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
]
