import re

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes

from user.models import User


from pprint import pp

from ..services.auth_services import AdminLoginService


def check_email_format(email):
    # 이메일 주소의 정규 표현식
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # 이메일 주소를 정규 표현식과 비교하여 검증
    return re.match(pattern, email)


from common.utils.response_formatter import JSONDataFormatter


class AdminLoginView(APIView):
    def post(self, request):
        res_formatter = JSONDataFormatter(200)
        response = Response()

        # 토큰을 통한 로그인이 아니면 이메일, 비밀번호 로그인 진행
        if not request.user.is_authenticated:
            AdminLoginService().login(res_formatter, request.data)
        else:
            res_formatter.message = "login by token"
        # res_formatter에 저장된 데이터를 response에 저장
        response.data = res_formatter.get_response_data()
        response.status_code = res_formatter.status
        return response
