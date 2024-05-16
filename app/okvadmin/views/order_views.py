from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order
from ..serializers.order_serializers import DummySerializer
from drf_spectacular.utils import extend_schema


class OrderTestView(APIView):
    
    @extend_schema(
        request=DummySerializer, responses={200: DummySerializer(many=True)}
    )
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
