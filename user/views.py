import re

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import *


def check_email_format(email):
    # 이메일 주소의 정규 표현식
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # 이메일 주소를 정규 표현식과 비교하여 검증
    return re.match(pattern, email)


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # 쿠키에 넣어주기...아직 어떤식으로 해야될지 모르겠는데 이렇게 설정만 우선 해주었다.
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:

            user = is_validated_token[0]
            res = Response(
                {
                    "name": user.name,
                    "eamil": user.email,
                    "phone_number": user.phone_number,
                    "birthday": user.birthday,
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    회원가입 된 계정으로 로그인하는 View
    """

    def post(self, request):
        # email값과 password값 받기
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            # 받아온 유저 토큰 생성
            token = TokenObtainPairSerializer.get_token(user)
            # settings -> restframe_work 부분에 timedelta로 유효기간 설정
            refresh_token = str(token)
            access_token = str(token.access_token)
            # 유저 정보와 로그인, 토큰 값들 Response
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        # 받아온 유저의 값이 없을 시
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # Authorization의 토큰 값과 유저의 토큰 값이 일치하는지 확인
    authentication_classes = [JWTAuthentication]  # simple-jwt JWTAuthentication 사용
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {"message": "Logout success"}, status=status.HTTP_202_ACCEPTED
        )
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class UpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]  # simple-jwt JWTAuthentication 사용
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 업데이트 가능

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # 사용자 정보 업데이트 전에 토큰 검증을 수행합니다.
        if not self.request.user.is_authenticated:
            return Response(
                {"error": "Invalid or missing token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Serializer를 사용하여 데이터를 업데이트
        serializer = self.get_serializer(
            instance=self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class DeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 현재 인증된 사용자 가져오기
            user = request.user
            # 사용자 삭제
            user.delete()
            return Response(
                {"message": "User data successfully deleted."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddressView(APIView):
    """
    주소 생성 및 조회 API
    """

    def post(self, request):
        """
        토큰 검증 이후 주소 생성 API
        """
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)
        if is_validated_token:
            user = is_validated_token[0]
            request.data["user_id"] = user.id
            # request.data["name"] = "home"
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(request.data)
                res = Response(
                    {
                        "address": serializer.data,
                        "message": "address create success",
                    },
                    status=status.HTTP_200_OK,
                )
                return res
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
        주소 유무에 따른 사용자 주소 조회 API
        """

        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            user = is_validated_token[0]
            address = Address.objects.filter(user=user.id).last()
            if address:
                res = {
                        "name": address.name,
                        "base": address.base,
                        "detail": address.detail,
                    }

                stat = status.HTTP_200_OK
            else:
                res = {
                    "error": "등록된 주소가 없습니다." 
                }
                stat = status.HTTP_400_BAD_REQUEST
            return Response(res, stat)
        return Response(status=status.HTTP_400_BAD_REQUEST)