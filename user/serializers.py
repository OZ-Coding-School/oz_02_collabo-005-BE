from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'phone_number', 'birthday']
        extra_kwargs = {'password': {'write_only': True}, # 패스워드 필드는 읽기 전용으로 설정
                        'birthday': {'required': False}
                        }  
