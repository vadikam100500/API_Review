from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "pk", "first_name",
            "last_name", "email", "role", "bio"
        )
