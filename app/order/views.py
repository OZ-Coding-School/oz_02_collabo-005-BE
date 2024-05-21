from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Order_detail, Order_option
from .serializers import *

from common.utils.response_formatter import JSONDataFormatter
from common.errors import CustomBadRequestError, CustomNegativeResponseWithData

from order.services import (
    CartCheckService,
    SaveOrderService,
    OrderDetailService,
    PaymentService,
)

from rest_framework.serializers import ValidationError
from django.db.utils import IntegrityError

from common.constants import StatusCode, Environments


class OrderCreateView(APIView):
    def post(self, request):
        # Formatter 생성
        formatter = JSONDataFormatter(201)

        try:
            order, payment = SaveOrderService(request).get_response_data()
            PaymentService(request, order, payment)
            response_data = {"code": order.order_status}
            if payment.status == StatusCode.PAYMENT_FAILED:
                response_data["fail"] = payment.cancle_reason
            formatter.add_response_data({"data": response_data})
        except CustomBadRequestError as e:
            formatter.set_status_and_message(e.status, e.message)
        except CustomNegativeResponseWithData as e:
            formatter.set_status_and_message(e.status, e.message)
            formatter.add_response_data({"data": e.data})
        except ValidationError as e:
            formatter.set_status_and_message(e.status_code, str(e))
        except IntegrityError as e:
            formatter.set_status_and_message(500, str(e))
        except Exception as e:
            formatter.set_status_and_message(500, str(e))

        return Response(formatter.get_response_data(), formatter.status)

from django.db.models import Q
class OrderListView(APIView):
    def get(self, request):
        formatter = JSONDataFormatter()

        user_id = request.user.id
        orders = Order.objects.filter( ~Q(order_status=StatusCode.ORDER_FAILED), user=user_id)
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
                total_price = detail_price * detail.quantity
                if restaurant.id in details_result:
                    details_result[restaurant.id]["quantity"] += detail.quantity
                    details_result[restaurant.id]["total_price"] += total_price
                else:
                    details_result[restaurant.id] = {
                        "restaurant_name": restaurant.name,
                        "menu_name": menu.name,
                        "quantity": detail.quantity,
                        "total_price": total_price,
                        "logo": (
                            Environments.OKIVERY_BUCKET_URL + restaurant.logo_image_url
                            if restaurant.logo_image_url
                            else None
                        ),
                    }

            result.append(
                {
                    "id": order.id,
                    "date": order.created_at.date(),
                    "order_status": order.order_status,
                    "details": details_result,
                }
            )

        formatter.add_response_data({"data": result})
        return Response(formatter.get_response_data(), status=formatter.status)


class OrderDetailView(APIView):
    def get(self, request):
        formatter = JSONDataFormatter()
        order_id = request.GET.get("id", None)

        if not order_id:
            return Response("Order id is required", status=400)

        try:
            formatter.add_response_data(
                {"data": OrderDetailService(order_id).get_response_data()}
            )
            formatter.message = "Check success"
        except CustomBadRequestError as e:
            formatter.set_status_and_message(e.status, e.message)
        except ValidationError as e:
            formatter.set_status_and_message(e.status_code, str(e))
        except Order.DoesNotExist as e:
            formatter.set_status_and_message(400, f"ID {order_id} is not exist")
        except IntegrityError as e:
            formatter.set_status_and_message(500, str(e))
        except Exception as e:
            print(type(e))
            formatter.set_status_and_message(500, str(e))

        return Response(formatter.get_response_data(), formatter.status)


class CartCheckView(APIView):
    def post(self, request):
        formatter = JSONDataFormatter()
        try:
            ccs = CartCheckService(request.data)
            formatter.add_response_data({"data": ccs.get_response_data()})
            formatter.message = "Request complete"
        except CustomBadRequestError as e:
            formatter.set_status_and_message(e.status, e.message)

        return Response(formatter.get_response_data(), status=formatter.status)
