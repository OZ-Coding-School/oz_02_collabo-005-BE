from rest_framework import serializers
from .models import User, Address


class UserSerializer(serializers.ModelSerializer):

    current_password = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    new_password = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
            "phone_number",
            "birthday",
            "current_password",
            "new_password",
        ]
        

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

        current_password = validated_data.pop("current_password", None)
        new_password = validated_data.pop("new_password", None)

        # current_password와 new_password가 모두 제공되었고, 빈 문자열이 아닌 경우에만 비밀번호 변경 로직 실행
        if current_password and new_password:
            if not instance.check_password(current_password):
                raise serializers.ValidationError(
                    {"current_password": "현재 비밀번호가 올바르지 않습니다."}
                )
            instance.set_password(new_password)
        elif current_password or new_password:
            # current_password 또는 new_password 중 하나만 제공된 경우 오류 발생
            raise serializers.ValidationError(
                {"passwords": "현재 비밀번호와 새 비밀번호 모두를 제공해야 합니다."}
            )



        return super().update(instance, validated_data)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["name", "base", "detail", "user_id"]
        depth = 1

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)

        return address
