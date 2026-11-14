from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson

User = get_user_model()


class LessonTestCase(APITestCase):
    """Тесты для CRUD уроков."""

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass123")
        self.course = Course.objects.create(name="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание урока",
            course=self.course,
            owner=self.user
        )
        # Аутентифицируем клиент
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тест создания урока."""
        url = reverse('lesson-list')
        data = {
            "name": "Новый урок",
            "description": "Описание",
            "video_link": "https://youtube.com/watch?v=123", # Валидная ссылка
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_with_invalid_link(self):
        """Тест создания урока с невалидной ссылкой (не youtube)."""
        url = reverse('lesson-list')
        data = {
            "name": "Урок с плохой ссылкой",
            "video_link": "https://rutube.ru/video/123",
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_retrieve_lesson(self):
        """Тест получения одного урока."""
        url = reverse('lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """Тест обновления урока."""
        url = reverse('lesson-detail', args=(self.lesson.pk,))
        data = {"name": "Обновленный урок"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновленный урок")

    def test_delete_lesson(self):
        """Тест удаления урока."""
        url = reverse('lesson-detail', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации."""
        self.client.force_authenticate(user=None)
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)