from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "payment_date", "paid_course", "paid_lesson", "amount", "payment_method"]


class UserSerializer(serializers.ModelSerializer):
    """Полный сериализатор профиля (для самого пользователя)."""
    payments_history = PaymentSerializer(many=True, read_only=True, source="payments")

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "last_name", "payments_history"]


class UserPublicSerializer(serializers.ModelSerializer):
    """Краткий сериализатор профиля (для просмотра другими пользователями)."""
    class Meta:
        model = User
        # Исключаем пароль, фамилию и историю платежей
        fields = ["id", "email", "phone", "city", "avatar"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'city']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            city=validated_data.get('city')
        )
        return user
