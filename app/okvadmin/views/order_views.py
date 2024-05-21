from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from okvadmin.permissions import IsStaffUser
from order.models import Order, Delivery, Payment
from ..serializers.order_serializers import (
    DummySerializer,
    OrderApproveSerializer,
    OrderCancleSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import timedelta
from django.utils import timezone

from common.constants import StatusCode, OrderConstants

from okvadmin.services.order_services import OrderListService


class OrderListView(APIView):
    permission_classes = [IsStaffUser]

    @extend_schema(request=DummySerializer, responses={200: DummySerializer(many=True)})
    def get(self, request):
        """
        주문 내역을 가져오는 API\n
        `new` 파라미터가 있으면
        `StatusCode.ORDER_PENDING`상태인 주문만 가져옴
        """
        oderListService = OrderListService()
        orders = oderListService.get_all()
        is_new = request.GET.get("new", None)
        print(is_new)
        if is_new == "1":
            orders = oderListService.get_new_list(orders)

        res = []
        for order in orders:
            print(order.get_order_status_display())
            data = {
                "id": order.id,
                "address": order.delivery_address,
                "status": order.get_order_status_display(),
                "price": order.order_price,
                "delivery_fee": order.delivery_fee,
                "total_price": order.total_price,
                "cancel_reason": order.cancle_reason,
                "time": int(order.created_at.timestamp() * 1000),
            }
            res.append(data)

        return Response(res, 200)


class OrderApprove(APIView):
    """
    주문 확인 후 소요시간 선택 및 배달확정하는 API
    is_self_delivery = 1 (자체배달) |
    is_self_delivery = 0 (배달업체)
    """

    @extend_schema(
        request=OrderApproveSerializer,
        responses={200: OrderApproveSerializer},
        examples=[
            OpenApiExample(
                "예시1",
                summary="배달 승인",
                description="배달 승인 시 cooking_time과 order_status 값 변화",
                value={
                    "order_id": 1,
                    "is_self_delivery": 1,
                    "time": 40,
                },
                request_only=True,
            )
        ],
    )
    def post(self, request, format=None):

        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)
        if is_validated_token:
            # 요청 데이터에서 필요한 정보 추출
            data = request.data
            order_id = data.get("order_id")
            is_self_delivery = data.get("is_self_delivery")
            time = data.get("time")  # Cooking time in minutes

            # order_id를 사용하여 Order 객체 조회
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response(
                    {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
                )

            # 같은 order_id 값이 있을 때 예외 처리
            if Delivery.objects.filter(order=order).exists():
                return Response(
                    {"message": "Order ID already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 승인된 경우
            current_time_korea = timezone.now()
            cooking_time_delta = timedelta(minutes=time)
            order.cooking_time = current_time_korea + cooking_time_delta
            order.order_status = StatusCode.ORDER_ACCEPTED
            order.save()

            # 주문에 연결된 배달 정보가 있는지 확인, 없으면 생성
            delivery, created = Delivery.objects.get_or_create(order=order)

            # 배달 정보 업데이트
            delivery.is_self_delivery = is_self_delivery
            delivery.delivery_status = StatusCode.DELIVERY_DISPATCH_PENDING
            delivery.estimated_time = order.cooking_time + timedelta(
                minutes=OrderConstants.DELIVERY_ESIMATED_MINUTE
            )
            delivery.save()

            # 직렬화 및 응답 반환
            return Response(
                {"message": "Order Approve successfully"}, status=status.HTTP_200_OK
            )


class OrderCancleView(APIView):

    @extend_schema(
        request=OrderCancleSerializer,
        responses={200: OrderCancleSerializer},
        examples=[
            OpenApiExample(
                "예시1",
                summary="배달 취소",
                description="배달 취소 시 cancle_reason 값 변화",
                value={
                    "order_id": 1,
                    "cancle_reason": "배불러서 취소",
                },
                request_only=True,
            )
        ],
    )
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            # 요청 데이터에서 필요한 정보 추출
            data = request.data
            order_id = data.get("order_id")
            status_code = data.get("status_code")
            cancle_reason = data.get("cancle_reason")

            # 상태 코드가 취소-가게, 취소-고객 중에 있는지 판단
            if status_code not in (
                StatusCode.ORDER_CANCELLED_BY_STORE,
                StatusCode.ORDER_CANCELLED_BY_CUSTOMER,
            ):
                return Response(
                    {"message": f"Status code {status_code} is invalid"}, status=400
                )

            # Order 객체 조회 및 상태 업데이트
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response(
                    {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
                )

            order.order_status = status_code  # 주문 상태를 결제 취소로 변경
            order.cancle_reason = cancle_reason  # 취소사유 수정
            order.save()

            # Delivery 객체 조회 및 상태 및 취소 시간 업데이트
            try:
                delivery = Delivery.objects.get(order=order)
                # 배달 상태를 주문_취소로 변경
                delivery.delivery_status = status_code
                delivery.cancle_time = timezone.now()  # 취소 시간 업데이트
                delivery.save()
            except Delivery.DoesNotExist:
                # Delivery 객체가 없으면 처리하지 않고 넘어감
                pass

            # Payment 객체 조회 및 상태 및 취소 이유 업데이트
            try:
                payment = Payment.objects.get(order=order)
                # 결제 상태를 결제 취소로 변경
                payment.status = StatusCode.PAYMENT_CANCELD
                # 취소사유를 주문취소로 변경
                payment.cancle_reason = status_code
                payment.save()
            except Payment.DoesNotExist:
                return Response(
                    {"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"message": "Order canceled successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Authentication failed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class OrderCooking(APIView):
    """
    주문 상태를 조리중으로 변경하는 API
    """

    def post(self, request, format=None):
        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if order.order_status != StatusCode.ORDER_ACCEPTED:
            return Response(
                {
                    "message": "Order is not in an accepted state",
                    "current_status": order.order_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.order_status = StatusCode.ORDER_COOKING
        order.save()

        return Response(
            {"message": "Order status updated to cooking"}, status=status.HTTP_200_OK
        )


class OrderCooked(APIView):
    """
    주문 상태를 조리완료로 변경하는 API
    """

    def post(self, request, format=None):
        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if order.order_status != StatusCode.ORDER_COOKING:
            return Response(
                {"message": "Order is not in a cooking state"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.order_status = StatusCode.ORDER_COOKED
        order.save()

        # order_delivery 테이블에서 delivery 정보를 가져오기
        try:
            delivery = Delivery.objects.get(order=order)
        except Delivery.DoesNotExist:
            return Response(
                {"message": "Delivery information not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # delivery_man_id에 따라 배달 상태 업데이트
        if delivery.delivery_man_id is None:
            delivery.delivery_status = StatusCode.DELIVERY_DISPATCH_PENDING
        else:
            delivery.delivery_status = StatusCode.DELIVERY_PICKUP_PENDING

        delivery.save()

        return Response(
            {
                "message": "Order status updated to cooked and delivery status updated",
                "status": f"{delivery.delivery_status}",
            },
            status=status.HTTP_200_OK,
        )


class AssignDelivery(APIView):
    """
    배달 기사가 배차를 요청하는 API
    """

    def post(self, request, format=None):
        order_id = request.data.get("order_id")
        delivery_man_id = request.data.get("delivery_man_id")

        try:
            # 주문 정보 가져오기
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 주문 상태 확인 (조리 중 또는 조리 완료 상태여야 함)
        if order.order_status not in [
            StatusCode.ORDER_COOKING,
            StatusCode.ORDER_COOKED,
        ]:
            return Response(
                {
                    "message": "Order is not in a valid state for delivery",
                    "current_status": order.order_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 배달 정보 가져오기
            delivery = Delivery.objects.get(order=order)
        except Delivery.DoesNotExist:
            return Response(
                {"message": "Delivery information not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 배달 상태 확인 (배차 대기 상태여야 함)
        if delivery.delivery_status != StatusCode.DELIVERY_DISPATCH_PENDING:
            return Response(
                {
                    "message": "Delivery is not in a dispatch pending state",
                    "current_status": delivery.delivery_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 배달 기사 ID 업데이트 및 배달 상태 변경
        delivery.delivery_man_id = delivery_man_id
        delivery.delivery_status = StatusCode.DELIVERY_PICKUP_PENDING

        delivery.save()

        return Response(
            {"message": "Delivery assigned and status updated to pickup pending"},
            status=status.HTTP_200_OK,
        )


class OrderDelivering(APIView):
    """
    주문 상태를 배달중으로 변경하는 API
    """

    def post(self, request, format=None):
        order_id = request.data.get("order_id")

        try:
            # 주문 정보 가져오기
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 주문 상태 확인
        if order.order_status != StatusCode.ORDER_COOKED:
            return Response(
                {
                    "message": "Order is not in a cooked state",
                    "current_status": order.order_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 배달 정보 가져오기
            delivery = Delivery.objects.get(order=order)
        except Delivery.DoesNotExist:
            return Response(
                {"message": "Delivery information not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 배달 상태 확인
        if delivery.delivery_status != StatusCode.DELIVERY_PICKUP_PENDING:
            return Response(
                {
                    "message": "Delivery is not in a pickup pending state",
                    "current_status": delivery.delivery_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 배달 상태를 배달중으로 업데이트
        order.order_status = (
            StatusCode.DELIVERY_DELIVERING
        )  # 주문 상태를 배달중으로 업데이트
        delivery.delivery_status = (
            StatusCode.DELIVERY_DELIVERING
        )  # 배달 상태를 배달중으로 업데이트

        order.save()
        delivery.save()

        return Response(
            {"message": "Order and delivery status updated to delivering"},
            status=status.HTTP_200_OK,
        )


class CompleteDelivery(APIView):
    """
    배달 상태를 배달완료로 변경하는 API
    """

    def post(self, request, format=None):
        order_id = request.data.get("order_id")

        try:
            # 주문 정보 가져오기
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 주문 상태 확인 (배달 중 상태여야 함)
        if order.order_status != StatusCode.DELIVERY_DELIVERING:
            return Response(
                {
                    "message": "Order is not in delivering state",
                    "current_status": order.order_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 배달 정보 가져오기
            delivery = Delivery.objects.get(order=order)
        except Delivery.DoesNotExist:
            return Response(
                {"message": "Delivery information not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 배달 상태 확인 (배달 중 상태여야 함)
        if delivery.delivery_status != StatusCode.DELIVERY_DELIVERING:
            return Response(
                {
                    "message": "Delivery is not in delivering state",
                    "current_status": delivery.delivery_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 주문 상태와 배달 상태를 배달 완료로 업데이트
        order.order_status = (
            StatusCode.DELIVERY_COMPLETED
        )  # 주문 상태를 배달 완료로 업데이트
        delivery.delivery_status = (
            StatusCode.DELIVERY_COMPLETED
        )  # 배달 상태를 배달 완료로 업데이트

        order.save()
        delivery.save()

        return Response(
            {"message": "Order and delivery status updated to delivered"},
            status=status.HTTP_200_OK,
        )
