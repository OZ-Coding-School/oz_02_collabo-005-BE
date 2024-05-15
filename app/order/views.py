import re

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Order, Order_detail, Order_option
from .serializers import *

from common.utils.geo_utils import (
    check_coordinate_in_polygon,
    get_coordinates_distance_km,
)
from common.utils.response_formatter import JSONDataFormatter
from common.errors import CustomError

from order.services import CartCheckService


class OrderCreateView(APIView):
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)
        if is_validated_token:
            coor = request.data.get("coordinate", None)
            if not coor:
                return Response(
                    {"code": 400, "message": "No coordinate"},
                    stat=status.HTTP_400_BAD_REQUEST,
                )

            if not check_coordinate_in_polygon(coor):
                res = {"code": 400, "message": "Coordinate is invalid"}
                stat = status.HTTP_400_BAD_REQUEST
            else:
                user = is_validated_token[0]
                request.data["user_id"] = user.id
                request.data.pop("coordinate")
                serializer = OrderSerializer(data=request.data)
                if serializer.is_valid():
                    a = serializer.create(request.data)
                    res = {"order": a.id, "message": "Success Created Order"}

                    distance = abs(
                        get_coordinates_distance_km(coor, (37.07967, 127.05227))
                    )
                    print(distance, a.total_price)
                    delivery_fee = 0
                    if a.total_price < 16900:
                        delivery_fee = 4400

                    if distance >= 1.5:
                        while distance > 0:
                            delivery_fee += 500
                            distance -= 0.5
                    res.update({"delivery_fee": delivery_fee})
                    stat = status.HTTP_201_CREATED
                    print(res)
                else:
                    res = {"error": serializer.errors}
                    stat = status.HTTP_400_BAD_REQUEST
        else:
            res = {"error": "Invalid token"}
            stat = status.HTTP_401_UNAUTHORIZED

        return Response(res, stat)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        formatter = JSONDataFormatter()

        user_id = request.user.id
        orders = Order.objects.filter(user=user_id)
        result = []
        for order in orders:
            details = Order_detail.objects.filter(order=order.id)
            details_result = {}
            for detail in details:
                menu = detail.menu
                detail_price = menu.price

                options = Order_option.objects.filter(order_detail=detail.id)
                for option in options:
                    detail_price += option.option_price

                restaurant = menu.restaurant
                if restaurant.id in details_result:
                    details_result[restaurant.id]["quantity"] += detail.quantity
                    details_result[restaurant.id]["total_price"] += detail_price
                else:
                    details_result[restaurant.id] = {
                        "menu_name": menu.name,
                        "quantity": detail.quantity,
                        "total_price": detail_price,
                        "logo": restaurant.logo_image_url,
                    }

            result.append(
                {
                    "id": order.id,
                    "date": order.created_at.date(),
                    "details": details_result,
                }
            )

        formatter.add_response_data({"data": result})
        return Response(formatter.get_response_data(), status=formatter.status)


class CartCheckView(APIView):
    def post(self, request):
        formatter = JSONDataFormatter()
        try:
            ccs = CartCheckService(request)
            formatter.add_response_data({"data": ccs.get_response_data()})
            formatter.message = "Request complete"
        except CustomError as e:
            formatter.set_status_and_message(e.status, e.message)

        return Response(formatter.get_response_data(), status=formatter.status)
