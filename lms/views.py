from rest_framework import viewsets
from lms.models import Course
from lms.serializers import CourseSerializer


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
