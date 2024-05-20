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


from restaurant.models import Restaurant, Menu, Option, Option_group_to_menu


class CartMenuCheckSerializers(serializers.Serializer):
    orders = serializers.ListField(child=serializers.DictField())

    def validate(self, data):
        validated_data = []
        for order in data.get("orders", []):
            order_data = {}
            restaurant_id = order.get("restaurant_id", None)
            if not restaurant_id:
                serializers.ValidationError(f"Restaurant id is required")
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
                order_data["restaurant"] = {
                    "id": restaurant_id,
                    "name": restaurant.name,
                    "status": restaurant.status,
                }
            except Restaurant.DoesNotExist:
                serializers.ValidationError(
                    f"Restaurant with id {menu_id} does not exist"
                )
            menus = order.get("menus", [])
            order_data["menus"] = []
            for menu_data in menus:
                menu_id = menu_data.get("id")
                quantity = menu_data.get("quantity", 0)

                # 1. 메뉴가 존재하는지 확인
                try:
                    menu = Menu.objects.get(id=menu_id)
                    # 메뉴가 식당에 존재하는지 확인
                    if menu.restaurant.pk != restaurant_id:
                        raise serializers.ValidationError(
                            f"This menu({menu_id}) does not restaurant({restaurant_id})'s menu"
                        )
                except Menu.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Menu with id {menu_id} does not exist"
                    )
                # 2. 메뉴가 존재하면 해당 메뉴의 (id, status, price)를 가져옴
                menu_info = {
                    "id": menu.id,
                    "name": menu.name,
                    "status": menu.status,
                    "price": menu.price,
                    "quantity": quantity,
                    "options": [],
                }

                # 3. 각 옵션의 유효성을 확인하고, 연결되어 있는지 확인
                options = menu_data.get("options", [])
                for option_id in options:
                    try:
                        option = Option.objects.get(id=option_id)
                    except Option.DoesNotExist:
                        raise serializers.ValidationError(
                            f"Option with id {option_id} does not exist"
                        )

                    if not Option_group_to_menu.objects.filter(
                        option_group_id=option.option_group_id, menu_id=menu_id
                    ).exists():
                        raise serializers.ValidationError(
                            f"Option with id {option_id} is not connected to the menu with id {menu_id}"
                        )

                    menu_info["options"].append(
                        {"id": option.id, "name": option.name, "price": option.price}
                    )
                order_data["menus"].append(menu_info)

            validated_data.append(order_data)

        return validated_data
