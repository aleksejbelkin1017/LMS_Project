from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_url

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "preview", "video_link", "course"]
        extra_kwargs = {
            "video_link": {"validators": [validate_youtube_url]}
        }

class CourseSerializer(serializers.ModelSerializer):
    # Задание 1: Поле для подсчета количества уроков
    lessons_count = serializers.SerializerMethodField()

    # Задание 3: Поле для вывода самих уроков (вложенный сериализатор)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # Важно: при добавлении кастомных полей нужно явно перечислить все поля
        fields = ["id", "name", "preview", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе."""
        return obj.lessons.count()
