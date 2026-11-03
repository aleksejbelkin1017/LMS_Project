from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Создает тестовые платежи"

    def handle(self, *args, **kwargs):
        # 1. Создаем пользователя (если нет)
        user, created = User.objects.get_or_create(
            email="student@example.com",
            defaults={"phone": "1234567890", "city": "Москва"}
        )
        if created:
            user.set_password("password123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Создан пользователь: {user.email}"))

        # 2. Создаем курс (если нет)
        course, created = Course.objects.get_or_create(
            name="Python-разработчик",
            defaults={"description": "Базовый курс по Python"}
        )

        # 3. Создаем урок (если нет)
        lesson, created = Lesson.objects.get_or_create(
            name="Введение в Django",
            course=course,
            defaults={"description": "Первый урок"}
        )

        # 4. Создаем платежи
        if not Payment.objects.exists():
            Payment.objects.create(
                user=user,
                paid_course=course,
                amount=50000.00,
                payment_method=Payment.PAYMENT_METHOD_TRANSFER
            )
            Payment.objects.create(
                user=user,
                paid_lesson=lesson,
                amount=5000.00,
                payment_method=Payment.PAYMENT_METHOD_CASH
            )
            self.stdout.write(self.style.SUCCESS("Создано 2 тестовых платежа."))
        else:
            self.stdout.write(self.style.WARNING("Платежи уже существуют в базе."))
