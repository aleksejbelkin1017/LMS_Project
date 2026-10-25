from rest_framework import viewsets, generics

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для полного CRUD курсов.
    Автоматически создает маршруты для:
    - GET /courses/ (список)
    - POST /courses/ (создание)
    - GET /courses/{id}/ (получение одного)
    - PUT /courses/{id}/ (обновление)
    - PATCH /courses/{id}/ (частичное обновление)
    - DELETE /courses/{id}/ (удаление)
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список всех уроков и создание нового (GET, POST)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока (GET, PUT, PATCH, DELETE)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
