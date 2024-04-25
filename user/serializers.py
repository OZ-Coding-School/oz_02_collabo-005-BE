from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "name", "phone_number", "birthday"]
        extra_kwargs = {
            "password": {"write_only": True},  # 패스워드 필드는 읽기 전용으로 설정
            "birthday": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # 비밀번호가 업데이트되는 경우에 대한 처리
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)
