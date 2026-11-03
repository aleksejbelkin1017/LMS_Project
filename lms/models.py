from django.db import models


class Course(models.Model):
    """Модель курса."""
    name = models.CharField(max_length=255, verbose_name="Название")
    preview = models.ImageField(upload_to="lms/courses/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока."""
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="lms/lessons/", blank=True, null=True, verbose_name="Превью")
    video_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на видео")

    # Связь с курсом (один курс - много уроков)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
