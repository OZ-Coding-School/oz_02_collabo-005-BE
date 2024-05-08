import re

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order
from .serializers import *


class TestView(APIView):
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            user = is_validated_token[0]
            request.data["user_id"] = user.id
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                a = serializer.create(request.data)

                
                res = {"order": a.id, "message": "Success Created Order"}
                stat = status.HTTP_201_CREATED
            else:
                res = {"error": serializer.errors}
                stat = status.HTTP_400_BAD_REQUEST
        else:
            res = {"error": "Invalid token"}
            stat = status.HTTP_401_UNAUTHORIZED

        return Response(res, stat)


# from rest_framework import mixins
# from rest_framework.viewsets import GenericViewSet

# from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework.permissions import IsAuthenticated
# from .models import Order
# from .serializers import *


# class OrderViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     GenericViewSet,
# ):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     authentication_classes = [JWTAuthentication]  # simple-jwt JWTAuthentication 사용
#     permission_classes = [IsAuthenticated]
#     def create(self, request, *args, **kwargs):
#         """
#         주문 생성


#         [req - model 데이터 일치 검증]
#         order_menu -> 이름, 가격
#         order_option_group -> 이름, mandatory, mandatory:true-> len(option_group) = 1,
#         order_option -> 이름, 가격

#         토큰 필요
#         """
#         return super().create(request, *args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         """
#         주문 조회


#         유저가 주문한 주문 조회
#         토큰 필요
#         """
#         return super().list(request, *args, **kwargs)

#     def retrieve(self, request, *args, **kwargs):
#         """
#         주문 디테일 조회


#         유저가 주문한 주문의 디테일 조회
#         토큰 필요
#         """
#         return super().retrieve(request, *args, **kwargs)

#     def get_serializer_class(self):
#         if self.action == "create":
#             return OrderCreateSerializer
#         if self.action == "retrieve":
#             return OrderSerializer
#         if self.action == "list":
#             return OrderListSerializer
#         return super().get_serializer_class()

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return (
#             qs.filter(user=self.request.user)
#         )

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


