from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
)

# Создаем роутер для ViewSet (Курсы)
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    # Маршруты для курсов (через роутер)
    path('', include(router.urls)),

    # Маршруты для уроков (через Generic)
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
]
