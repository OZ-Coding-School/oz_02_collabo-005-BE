from rest_framework import serializers
from order.models import Order, Delivery

class DummySerializer(serializers.Serializer):
    pass

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["delivery_man_id", "estimated_time"]


class OrderApproveSerializer(serializers.ModelSerializer):
    delivery = DeliverySerializer(read_only=True)
    class Meta:
        model = Order
        fields = ["id", "cooking_time", "order_status", "delivery"]
