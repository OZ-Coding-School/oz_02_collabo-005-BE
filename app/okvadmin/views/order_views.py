from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order, Delivery
from ..serializers.order_serializers import DummySerializer, OrderApproveSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import timedelta
from django.utils import timezone


class OrderTestView(APIView):

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
                    "refuse": False,
                    "time": 40,
                },
                request_only=True,
            ),
            OpenApiExample(
                "예시2",
                summary="배달 거절",
                description="배달 거절 시 order_status 값 변화",
                value={"order_id": 1, "refuse": True},
                request_only=True,
            ),
        ],
    )
    def post(self, request, format=None):
        # 요청 데이터에서 필요한 정보 추출
        data = request.data
        order_id = data.get("order_id")
        refuse = data.get("refuse")
        time = data.get("time")  # Cooking time


        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        # 같은 order_id 값이 있을 떄 예외처리 해주기
        if Delivery.objects.filter(order=order).exists():
            return Response(
                {"message": "Order ID already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if refuse:
            # 거부된 경우, 주문 상태 업데이트
            order.order_status = 23
            order.save()
        else:
            # 승인된 경우
            current_time_korea = timezone.now()
            cooking_time_delta = timedelta(minutes=time)
            order.cooking_time = current_time_korea + cooking_time_delta
            order.order_status = 21
            order.save()

            # 주문에 연결된 배달 정보가 있는지 확인, 없으면 생성
            if hasattr(order, "delivery"):
                delivery = order.delivery
            else:
                delivery = Delivery(order=order)

            # 배달 정보 업데이트
            delivery.estimated_time = order.cooking_time + timedelta(
                minutes=30
            )
            delivery.save()

        serializer = OrderApproveSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
