from rest_framework import serializers

def validate_youtube_url(value):
    """Проверяет, что ссылка ведет только на YouTube."""
    if value and 'youtube.com' not in value:
        raise serializers.ValidationError(
            "Ссылка должна вести только на ресурс youtube.com"
        )
    return value
