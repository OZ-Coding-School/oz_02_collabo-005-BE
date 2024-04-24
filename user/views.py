from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from .serializers import *
from django.http import JsonResponse
import re


def check_email_format(email):
    # 이메일 주소의 정규 표현식
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # 이메일 주소를 정규 표현식과 비교하여 검증
    return re.match(pattern, email)


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            name = serializer.validated_data["name"]
            phone_number = serializer.validated_data["phone_number"]
            birthday = serializer.validated_data.get("birthday")

            # 일반 사용자 생성
            user = User.objects.create_user(
                email=email,
                password=password,
                name=name,
                phone_number=phone_number,
                birthday=birthday,
            )

            # 혹은 슈퍼유저 생성
            # user = User.objects.create_superuser(email=email, password=password, name=name, phone_number=phone_number, birthday=birthday)

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    """
    이메일의 중복여부 체크 View
    """

    def get(self, request):
        email = request.GET.get("email", None)
        if email:
            # 이메일 형식 체크
            if not check_email_format(email):
                return JsonResponse(
                    {"error": "이메일 형식이 맞지 않습니다."}, status=403
                )

            # 이메일 중복 체크
            user_exists = User.objects.filter(email=email).exists()

            # 중복 이메일이 있을시
            if user_exists:
                return JsonResponse({"email": email, "exists": True})

            # 중복 이메일이 없을시
            return JsonResponse({"email": email, "exists": False})

        return JsonResponse({"error": "Email parameter is missing"}, status=400)


class LoginView(APIView):
    """
    여기서 사용자 이름과 비밀번호를 확인하여 유효성을 검사합니다.
    만약 검증에 성공하면 사용자 정보를 가져오고, 아니면 에러 응답을 반환합니다.

    예시로 사용자 정보를 가져오는 대신, 단순히 고정된 사용자를 사용합니다.
    """

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 사용자 인증
        user = authenticate(email=email, password=password)
        if user is not None:
            # 사용자 인증 성공 시, 액세스 토큰 생성
            access_token = AccessToken.for_user(user)
            return Response({"access_token": str(access_token)})
        else:
            # 사용자 인증 실패 시
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
