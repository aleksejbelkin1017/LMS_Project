from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
]
