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

from order.services import CartCheckService, SaveOrderService, PaymentService

from rest_framework.serializers import ValidationError
from django.db.utils import IntegrityError

class OrderCreateView(APIView):
    def post(self, request):
        # Formatter 생성
        formatter = JSONDataFormatter(201)

        # 유저가 보낸 카드정보 체크 (?) - 일단 보류

        # 유저가 보낸 데이터 검증(주문데이터가 정확한지)
        try:
            order, payment = SaveOrderService(request).get_response_data()
            PaymentService(request, order, payment)
            response_data = {"code": payment.status}
            if payment.status == "PMS002":
                response_data['fail'] = payment.failure_reason
            formatter.add_response_data({"data": response_data})
        except CustomError as e:
            formatter.set_status_and_message(e.status, e.message)
        except ValidationError as e:
            formatter.set_status_and_message(e.status_code, str(e))
        except IntegrityError as e:
            formatter.set_status_and_message(500, str(e))
        except Exception as e:
            formatter.set_status_and_message(500, str(e))

        # 검증된 데이터에 추가적인 정보(request, address 등)을 붙여서 order 생성 (결제대기 상태)

        # order에 등록되면 결제 진행
        # 결제가 구현이 되어있지 않으므로 결제는 확률적으로 실패

        # 결제 여부에 따라 order에 status 변경 + 취소시 취소사유(cancle_reason) 추가

        # 성공, 실패 여부 return

        return Response(formatter.get_response_data(), formatter.status)


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
                        "restaurant_name": restaurant.name,
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
