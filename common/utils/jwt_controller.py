from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user_id, claims):
        user = User.objects.get(id=user_id)
        token = super().get_token(user)

        for key, value in claims.items():
            token[key] = value

        return token


class TokenCreator:
    @classmethod
    def create_token_by_data(cls, user_id, claims):
        return CustomTokenObtainPairSerializer.get_token(user_id, claims)
    
    @classmethod
    def create_token_by_token(cls, old_refresh_token):
        return RefreshToken(old_refresh_token)
