from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order, Delivery, Payment
from ..serializers.order_serializers import DummySerializer, OrderApproveSerializer, OrderCancleSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import timedelta
from django.utils import timezone


class OrderGetListView(APIView):

    @extend_schema(request=DummySerializer, responses={200: DummySerializer(many=True)})
    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        order_data = []
        if is_validated_token:
            # 유효한 토큰일 경우 주문 정보 조회
            orders = Order.objects.all().order_by("order_status")
            for order in orders:
                if order.order_status >= 20:
                    res = {"order_id": order.id, "order_status": order.order_status}
                    order_data.append(res)
            return Response(order_data, status=status.HTTP_200_OK)


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
        ]
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
                    {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
                )
            
            # 같은 order_id 값이 있을 때 예외 처리
            if Delivery.objects.filter(order=order).exists():
                return Response(
                    {"message": "Order ID already exists"}, status=status.HTTP_400_BAD_REQUEST
                )

            # 승인된 경우
            current_time_korea = timezone.now()
            cooking_time_delta = timedelta(minutes=time)
            order.cooking_time = current_time_korea + cooking_time_delta
            order.order_status = 21
            order.save()

            # 주문에 연결된 배달 정보가 있는지 확인, 없으면 생성
            delivery, created = Delivery.objects.get_or_create(order=order)

            # 배달 정보 업데이트
            delivery.is_self_delivery = is_self_delivery
            delivery.delivery_status = 21
            delivery.estimated_time = order.cooking_time + timedelta(minutes=30)
            delivery.save()

            # 직렬화 및 응답 반환
            return Response(
                {"message": "Order Approve successfully"},
                status=status.HTTP_200_OK
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
        ]
    )
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            # 요청 데이터에서 필요한 정보 추출
            data = request.data
            order_id = data.get("order_id")
            cancle_reason = data.get("cancle_reason")

            # Order 객체 조회 및 상태 업데이트
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response(
                    {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
                )
            
            order.order_status = 23  # 주문 상태를 취소(23)로 변경
            order.cancle_reason = cancle_reason
            order.save()

            # Delivery 객체 조회 및 상태 및 취소 시간 업데이트
            delivery = Delivery.objects.get(order=order)
            delivery.delivery_status = 23  # 배달 상태를 취소(23)로 변경
            delivery.cancle_time = timezone.now()  # 취소 시간 업데이트
            delivery.save()

            # Payment 객체 조회 및 상태 및 취소 이유 업데이트
            payment = Payment.objects.get(order=order)
            payment.status = "PMS003"  # 결제 상태를 취소 상태로 변경
            payment.cancle_reason = "PMF600"  # 취소 이유 업데이트
            payment.save()

            return Response(
                {"message": "Order canceled successfully"},
                status=status.HTTP_200_OK
            )