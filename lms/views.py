from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD курсов с разграничением прав."""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        """Настраиваем права в зависимости от действия (action)."""
        if self.action == 'create':
            # Создавать может только авторизованный пользователь, НЕ модератор
            return [IsAuthenticated(), ~IsModerator()]
        elif self.action in ['update', 'partial_update']:
            # Редактировать может модератор ИЛИ владелец
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.action == 'destroy':
            # Удалять может только владелец (модератор не может)
            return [IsAuthenticated(), IsOwner()]

        # На просмотр (list, retrieve) — только авторизованные
        return [IsAuthenticated()]

    def get_queryset(self):
        """Модераторы видят все курсы, остальные — только свои."""
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """При создании автоматически назначаем владельца."""
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список всех уроков и создание нового (GET, POST)."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            # Создавать может только авторизованный пользователь, НЕ модератор
            return [IsAuthenticated(), ~IsModerator()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Модераторы видят все уроки, остальные — только свои."""
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """При создании автоматически назначаем владельца."""
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока (GET, PUT, PATCH, DELETE)."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            # Редактировать может модератор ИЛИ владелец
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.request.method == 'DELETE':
            # Удалять может только владелец (модератор не может)
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Модераторы видят все уроки, остальные — только свои."""
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)
