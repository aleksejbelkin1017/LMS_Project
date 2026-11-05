from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "payment_date", "paid_course", "paid_lesson", "amount", "payment_method"]


class UserSerializer(serializers.ModelSerializer):
    # Доп. задание: добавляем историю платежей
    # source="payments" — это related_name из модели Payment
    payments_history = PaymentSerializer(many=True, read_only=True, source="payments")

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "payments_history"]
