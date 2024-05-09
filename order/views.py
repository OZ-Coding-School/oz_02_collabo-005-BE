import re

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order
from .serializers import *


class OrderCreateView(APIView):
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


class OrderGetListView(APIView):
    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            user = is_validated_token[0]
            orders = Order.objects.filter(user=user.id)
            response_data = []
            for order in orders:
                detail_menu_list = []
                order_detail_ids = Order_detail.objects.filter(order=order.id)

                for order_detail in order_detail_ids:
                    menu_id = order_detail.menu_id
                    menu = Menu.objects.get(id=menu_id)
                    restaurant = menu.restaurant
                    total_price = menu.price * order_detail.quantity
                    options_list = []

                    order_options = Order_option.objects.filter(order_detail=order_detail)
                    for order_option in order_options:
                        options_res = {"option_name": order_option.option_name}
                        options_list.append(options_res)
                        total_price += order_option.option_price

                    menu_res = {
                        "name": menu.name,
                        "quantity": order_detail.quantity,
                        "option": options_list,
                        "total_price": total_price,
                    }

                    restaurant_res = {
                        "restaurant_id": restaurant.id,
                        "restaurant_name": restaurant.name,
                        "picture": restaurant.representative_menu_picture,
                        "menu_name": menu_res,
                    }

                    detail_menu_list.append(restaurant_res)

                res = {
                    "id": order.id,
                    "order_time": order.order_time,
                    "user_id": order.user_id,
                    "menus": detail_menu_list,
                }
                response_data.append(res)
            return Response(response_data)

