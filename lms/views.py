from lms.paginators import MyPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD курсов с разграничением прав."""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def get_permissions(self):
        """Настраиваем права в зависимости от действия (action)."""
        if self.action == 'create':
            # Создавать может только авторизованный пользователь, НЕ модератор
            return [IsAuthenticated(), (~IsModerator)()]
        elif self.action in ['update', 'partial_update']:
            # Редактировать может модератор ИЛИ владелец
            return [IsAuthenticated(), (IsModerator | IsOwner)()]
        elif self.action == 'destroy':
            # Удалять может только владелец (модератор не может)
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список всех уроков и создание нового (GET, POST)."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MyPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            # Создавать может только авторизованный пользователь, НЕ модератор
            return [IsAuthenticated(), (~IsModerator)()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока (GET, PUT, PATCH, DELETE)."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            # Редактировать может модератор ИЛИ владелец
            return [IsAuthenticated(), (IsModerator | IsOwner)()]
        elif self.request.method == 'DELETE':
            # Удалять может только владелец (модератор не может)
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class SubscriptionAPIView(APIView):
    """Управление подпиской на курс (создание/удаление)."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"error": "Не передан course_id"}, status=400)

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message})
