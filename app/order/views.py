from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Order_detail, Order_option
from .serializers import *

from common.utils.response_formatter import JSONDataFormatter
from common.errors import CustomError

from order.services import CartCheckService, SaveOrderService, PaymentService

from rest_framework.serializers import ValidationError
from django.db.utils import IntegrityError


class OrderCreateView(APIView):
    def post(self, request):
        # Formatter 생성
        formatter = JSONDataFormatter(201)

        try:
            order, payment = SaveOrderService(request).get_response_data()
            PaymentService(request, order, payment)
            response_data = {"code": payment.status}
            if payment.status == "PMS002":
                response_data["fail"] = payment.failure_reason
            formatter.add_response_data({"data": response_data})
        except CustomError as e:
            formatter.set_status_and_message(e.status, e.message)
        except ValidationError as e:
            formatter.set_status_and_message(e.status_code, str(e))
        except IntegrityError as e:
            formatter.set_status_and_message(500, str(e))
        except Exception as e:
            formatter.set_status_and_message(500, str(e))

        return Response(formatter.get_response_data(), formatter.status)


class OrderListView(APIView):
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
                        "logo": restaurant.logo_image_url,
                    }

            print(
                restaurant.name,
                menu.name,
                detail.quantity,
                details_result[restaurant.id]["total_price"],
            )
            result.append(
                {
                    "id": order.id,
                    "date": order.created_at.date(),
                    "details": details_result,
                }
            )

        formatter.add_response_data({"data": result})
        return Response(formatter.get_response_data(), status=formatter.status)


class OrderDetailView(APIView):
    def get(self, request):
        pass


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
