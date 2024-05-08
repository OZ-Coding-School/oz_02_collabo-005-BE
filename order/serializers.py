from rest_framework import serializers
from order.models import Order, Order_detail, Order_option
from restaurant.models import *


class OrderOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_option
        fields = ("id", "option_name", "option_price", "option_group_name")
        extra_kwargs = {
            "option_name": {"required": False},
            "option_price": {"required": False},
            "option_group_name": {"required": False},
        }


class OrderDetailSerializer(serializers.ModelSerializer):
    order_options = OrderOptionSerializer(many=True, required=False)

    class Meta:
        model = Order_detail
        fields = ["id", "menu", "quantity", "order_options"]


class OrderListSerializer(serializers.ModelSerializer):
    """주문 내역 리스트"""

    class Meta:
        model = Order
        fields = (
            "id",
            "order_menu",
            "order_status",
            "order_time",
        )


class OrderSerializer(serializers.ModelSerializer):

    order_menu = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "order_menu",
            "order_status",
            "delivery_address",
            "total_price",
            "store_request",
            "rider_request",
            "user_id",
        ]
        extra_kwargs = {
            "cooking_time": {"required": False},
            "dispatch_status": {"required": False},
            "store_request": {"required": False},
            "rider_request": {"required": False},
            "cancle_reason": {"required": False},
            "order_status": {"required": False},
            "total_price": {"required": False},
        }

    def create(self, validated_data):
        validated_data.setdefault("order_status", 1)
        order_menus_data = validated_data.pop("order_menu")
        # 주문 시작 시 총 가격을 0으로 설정
        total_price = 0
        order = Order.objects.create(**validated_data)

        for order_menu_data in order_menus_data:
            # 'menu'는 외래키이므로, 해당 ID로 Menu 객체 찾기
            menu_id = order_menu_data.pop("menu")
            menu = Menu.objects.get(id=menu_id)
            order_options = order_menu_data.pop("order_options", [])
            quantity = order_menu_data.get("quantity", 1)  # 수량 정보 가져오기
            # 메뉴 가격에 수량을 곱해 총 가격에 추가
            total_price += menu.price * quantity
            order_detail = Order_detail.objects.create(
                order=order, menu=menu, **order_menu_data
            )

            for order_option in order_options:
                group_id = order_option.get("group")
                option_group_name = Option_group.objects.get(id=group_id).name

                for option_id in order_option.get("options", []):
                    option = Option.objects.get(id=option_id)

                    Order_option.objects.create(
                        order_detail=order_detail,
                        option_group_name=option_group_name,
                        option_price=option.price,
                        option_name=option.name,
                    )
                    # 옵션 가격을 총 가격에 추가
                    total_price += option.price

        # 총 가격을 주문 객체에 저장
        order.total_price = total_price
        order.save()

        return order
