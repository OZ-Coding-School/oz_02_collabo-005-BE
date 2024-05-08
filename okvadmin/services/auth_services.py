from rest_framework import status

from okvadmin.serializers.auth_serializers import AdminLoginValidSerializer
from common.utils.jwt_controller import TokenCreator


class AdminLoginService:
    def get_serializer_data(self, request_data):
        serializer = AdminLoginValidSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def get_token(self, data):
        refresh_token = TokenCreator.create_token_by_data(data.get("id"), data)

        return {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token),
        }
    
    def login(self, res_formatter, request_data):
        s_data = self.get_serializer_data(request_data)

        if s_data["is_staff"]:
            res_formatter.message = "login by email"
            res_formatter.add_response_data(self.get_token(s_data))
        else:
            res_formatter.message = "you are not staff"
            res_formatter.status = status.HTTP_401_UNAUTHORIZED
