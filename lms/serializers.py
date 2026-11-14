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
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons_count", "lessons", "is_subscribed", "owner"]
        read_only_fields = ["owner"] # <-- Это обязательно должно быть здесь

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscriptions.filter(user=request.user).exists()
        return False
