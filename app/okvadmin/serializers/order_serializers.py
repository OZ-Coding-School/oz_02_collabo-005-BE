from rest_framework import serializers
from order.models import Order, Delivery

class DummySerializer(serializers.Serializer):
    pass

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["is_self_delivery"]


class OrderApproveSerializer(serializers.ModelSerializer):
    delivery = DeliverySerializer(read_only=True)
    class Meta:
        model = Order
        fields = ["id", "cooking_time", "order_status", "delivery"]

class OrderCancleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "cancle_reason"]
