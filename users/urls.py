from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    PaymentListAPIView,
)

urlpatterns = [
    # JWT-авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # CRUD для пользователей
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Платежи
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
]
