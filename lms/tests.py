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


class SubscriptionTestCase(APITestCase):
    """Тесты для функционала подписки на курс."""

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create_user(email="subuser@example.com", password="testpass123")
        self.course = Course.objects.create(name="Курс для подписки", owner=self.user)

        # Второй пользователь для теста чужих действий
        self.other_user = User.objects.create_user(email="other@example.com", password="testpass123")

        # Аутентифицируем первого пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """Тест создания подписки."""
        url = reverse('subscription')
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Подписка добавлена")
        self.assertTrue(self.user.subscriptions.filter(course=self.course).exists())

    def test_delete_subscription(self):
        """Тест удаления подписки (повторный запрос)."""
        url = reverse('subscription')
        data = {"course_id": self.course.id}

        # Создаем подписку
        self.client.post(url, data)
        # Удаляем
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Подписка удалена")
        self.assertFalse(self.user.subscriptions.filter(course=self.course).exists())

    def test_is_subscribed_field(self):
        """Тест отображения статуса подписки в курсе."""
        # Создаем подписку через модель
        self.user.subscriptions.create(course=self.course)

        url = reverse('courses-detail', args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

    def test_subscription_unauthorized(self):
        """Тест доступа к подписке без авторизации."""
        self.client.force_authenticate(user=None)
        url = reverse('subscription')
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
