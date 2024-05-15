import re

from drf_spectacular.utils import extend_schema
from django.utils import timezone
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
    """
    POST - 유저를 생성하는 뷰
    GET - 생성된 유저를 토큰에 따라서 조회하는 뷰
    """

    @extend_schema(request=UserSerializer, responses={200: UserSerializer})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            res = Response(
                {
                    "message": "create success",
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:

            user = is_validated_token[0]
            res = Response(
                {
                    "name": user.name,
                    "email": user.email,
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

    @extend_schema(request=DummySerializer, responses={200: DummySerializer(many=False)})
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

    @extend_schema(request=UserLoginSerializer, responses={200: UserLoginSerializer(many=False)})
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 이메일이나 비밀번호가 제공되지 않았을 경우
        if not email or not password:
            return Response(
                {"error": "이메일과 비밀번호를 모두 제공해야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        # user가 존재하지만 deleted_at 필드에 값이 설정되어 있는 경우
        if user is not None and user.deleted_at is not None:
            return Response(
                {"error": "삭제된 사용자입니다."},
                status=status.HTTP_200_OK,
            )

        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(
                {"error": "잘못된 이메일 또는 비밀번호입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    # Authorization의 토큰 값과 유저의 토큰 값이 일치하는지 확인
    authentication_classes = [JWTAuthentication]  # simple-jwt JWTAuthentication 사용
    permission_classes = [IsAuthenticated]

    @extend_schema(request=DummySerializer, responses={200: DummySerializer(many=False)})
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {"message": "Logout success"}, status=status.HTTP_202_ACCEPTED
        )
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class UpdateView(UpdateAPIView):
    """
    유저 정보를 업데이트 하는 View
    current_password와 new_password가 모두 비워져 있을땐 다른 정보를 업데이트
    """
    serializer_class = UserUpdateSerializer
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

        return Response({"Update Complate", status.HTTP_200_OK})


class DeleteView(APIView):
    """
    유저 데이터 삭제
    delete_at 데이터베이스에 추가
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(request=DummySerializer, responses={200: DummySerializer(many=False)})
    def post(self, request):
        try:
            # 현재 인증된 사용자 가져오기
            user = request.user
            # 사용자 삭제 대신 deleted_at 필드 설정
            user.deleted_at = timezone.now()
            user.save()
            return Response(
                {"message": "User data successfully soft deleted."},
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
    serializer_class = AddressSerializer 
    
    @extend_schema(request=AddressSerializer, responses={200: AddressSerializer(many=False)})
    def post(self, request):
        """
        POST - 토큰 검증 이후 주소 생성 API
        GET - 토큰 검증 이후 주소 조회
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
                res = {"error": "등록된 주소가 없습니다."}
                stat = status.HTTP_400_BAD_REQUEST
            return Response(res, stat)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(APIView):
    """
    주소 업데이트 뷰
    """
    @extend_schema(request=AddressSerializer, responses={200: AddressSerializer(many=False)})
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            user = is_validated_token[0]
            address = Address.objects.filter(user=user.id).last()

            if address:
                serializer = AddressSerializer(address, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"error": "등록된 주소 정보가 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(status=status.HTTP_400_BAD_REQUEST)


from common.utils.geo_utils import check_coordinate_in_polygon


class AddressCoordinateWithinPolygonView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=DummySerializer, responses={200: DummySerializer(many=False)})
    def get(self, request):
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        if not lat or not lng:
            return Response(
                {"code": 400, "message": "No lat or lng"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        coor = (lat, lng)
        return Response(
            {
                "code": 200,
                "message": "Check coordinate is success",
                "data": {"result": check_coordinate_in_polygon(coor)},
            }
        )
