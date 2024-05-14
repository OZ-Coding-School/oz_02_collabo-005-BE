from rest_framework.response import Response
from rest_framework import status
from abc import ABCMeta, abstractmethod


class BasicServiceClass(metaclass=ABCMeta):
    def __init__(self, request=None):
        super().__init__()
        self.request = request
        self.response_data = None

    def get_response_data(self):
        return self.response_data

    @abstractmethod
    def is_valid():
        pass


from common.errors import CustomBadRequestError
from common.utils.geo_utils import (
    check_coordinate_in_polygon,
    get_coordinates_distance_km,
)
from restaurant.models import Menu, Option_group_to_menu
from pprint import pp
from .serializers import CartMenuCheckSerializers


class OrderServiceUtils:
    def get_menu_price(self, menu):
        option_price = 0
        for option in menu["options"]:
            option_price += option["price"]
        return (menu["price"] + option_price) * menu["quantity"]

    def get_order_price(self, menus):
        result = 0
        for menu in menus:
            if menu["status"]:
                result += self.get_menu_price(menu)
        return sum((self.get_menu_price(menu) for menu in menus), 0)

    def get_delivery_fee(self, coor, order_price):
        OKIVERY_COOR = (37.07967, 127.05227)
        distance = abs(get_coordinates_distance_km(coor, OKIVERY_COOR))
        delivery_fee = 0
        if order_price < 16900:
            delivery_fee = 4400

        if distance >= 1.5:
            while distance >= 0:
                delivery_fee += 500
                distance -= 0.5
        return delivery_fee


class CartCheckService(BasicServiceClass):
    def __init__(self, request):
        super().__init__(request)
        validated_data = self.is_valid()
        self.response_data = self.set_price_data(validated_data)

    def is_valid(self):
        multiple_menu_serializer = CartMenuCheckSerializers(data=self.request.data)
        multiple_menu_serializer.is_valid(raise_exception=True)

        menu_data = multiple_menu_serializer.validated_data
        result = {"menus": menu_data}

        coor = self.request.data.get("coordinate", None)
        if not coor:
            result["coordinate"] = False
        else:
            if type(coor) != list:
                raise CustomBadRequestError(
                    "Coordinate format is worng. It must be list"
                )
            elif len(coor) != 2:
                raise CustomBadRequestError(
                    "Coordinate must contain only two values - [lat, lng]"
                )
            elif not all(isinstance(item, (int, float)) for item in coor):
                raise CustomBadRequestError(
                    "Coordinate must contain only int or float types"
                )

            result["coordinate"] = check_coordinate_in_polygon(coor)
        return result

    def set_price_data(self, data):
        osu = OrderServiceUtils()
        order_price = 0
        for menu in data['menus']:
            menu_price = 0
            if menu['status']:
                menu_price = osu.get_menu_price(menu)
            menu['menu_total_price'] = menu_price
            order_price += menu_price

        coor = self.request.data.get("coordinate", None)
        if coor:
            delivery_fee = osu.get_delivery_fee(
                self.request.data["coordinate"], order_price
            )
        else:
            delivery_fee = 0
        data["order_price"] = order_price
        data["delivery_fee"] = delivery_fee
        data["total_price"] = order_price + delivery_fee
        return data
