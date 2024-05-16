from rest_framework import serializers
from order.models import Order

class DummySerializer(serializers.Serializer):
    pass

class OrderApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "cooking_time", "order_status"]
        example = {
            "id": 1,
            "cooking_time": "40",
            "order_status": 20
        }

# class OrderApproveSerializer(serializers.Serializer):
#     id = serializers.IntegerField(help_text="주문 ID", example=1)
#     refuse = serializers.BooleanField(help_text="주문 거절 여부", example=False)
#     time = serializers.IntegerField(help_text="추가 시간(분)", example=40)

#     class Meta:
#         fields = ['id', 'refuse', 'time']