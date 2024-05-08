from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from user.models import User


class AdminLoginValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_staff", "last_login"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "last_login": {"read_only": True},
        }

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found"
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # return {
        #     "email": user.email,
        #     "is_staff": user.is_staff,
        #     "last_login": user.last_login,
        # }
        return user
