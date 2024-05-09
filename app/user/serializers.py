from rest_framework import serializers
from .models import User, Address


class UserSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["email", "password", "name", "phone_number", "birthday", "current_password", "new_password"]
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
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)

        if current_password and new_password:
            if not instance.check_password(current_password):
                raise serializers.ValidationError({'current_password': '현재 비밀번호가 올바르지 않습니다.'})
            instance.set_password(new_password)

        return super().update(instance, validated_data)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["name", "base", "detail", "user_id"]
        depth = 1

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)

        return address
