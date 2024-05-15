from rest_framework import serializers
from .models import User, Address
from .utils import validate_password, validate_phone_number, validate_birthday

import re

class DummySerializer(serializers.Serializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
            "phone_number",
            "birthday",
        ]

        extra_kwargs = {
            "password": {"write_only": True},  # 패스워드 필드는 읽기 전용으로 설정
            "birthday": {"required": False},
        }

    def validate(self, data):
        # 각 필드의 유효성 검사 수행
        password = data.get("password")
        phone_number = data.get("phone_number")
        birthday = data.get("birthday")

        if password:
            validate_password(password)

        if phone_number:
            validate_phone_number(phone_number)

        if birthday:
            validate_birthday(birthday)
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "phone_number",
            "birthday",
            "current_password",
            "new_password",
        ]

    def validate(self, data):
        new_password = data.get("new_password")
        phone_number = data.get("phone_number")
        birthday = data.get("birthday")

        if new_password:
            validate_password(new_password)

        if phone_number:
            validate_phone_number(phone_number)

        if birthday:
            validate_birthday(birthday)
        
        return data

    def update(self, instance, validated_data):
        current_password = validated_data.pop("current_password", None)
        new_password = validated_data.pop("new_password", None)

        # 비밀번호 변경 로직
        if current_password or new_password:
            if not current_password:
                raise serializers.ValidationError(
                    {"current_password": "현재 비밀번호를 입력해야 합니다."}
                )
            if not instance.check_password(current_password):
                raise serializers.ValidationError(
                    {"current_password": "현재 비밀번호가 올바르지 않습니다."}
                )
            if new_password:
                instance.set_password(new_password)

        # 나머지 필드 업데이트
        return super(UserUpdateSerializer, self).update(instance, validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["name", "base", "detail", "user_id"]
        depth = 1

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)

        return address
