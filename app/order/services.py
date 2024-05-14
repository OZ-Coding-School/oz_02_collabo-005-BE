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
from common.utils.geo_utils import check_coordinate_in_polygon
from restaurant.models import Menu, Option_group_to_menu
from pprint import pp
from .serializers import CartMenuCheckSerializers


class CartCheckService(BasicServiceClass):
    def __init__(self, request):
        super().__init__(request)
        self.response_data = {}
        self.is_valid()

    def is_valid(self):
        multiple_menu_serializer = CartMenuCheckSerializers(data=self.request.data)
        multiple_menu_serializer.is_valid(raise_exception=True)

        menu_data = multiple_menu_serializer.validated_data
        print(type(menu_data), type(self.response_data))
        result = {"menus": menu_data}

        coor = self.request.data.get("coordinate", None)
        print(coor)
        print(coor, type(coor), type(coor[0]))
        if not coor:
            raise CustomBadRequestError("Coordinate is required")
        elif type(coor) != list:
            raise CustomBadRequestError("Coordinate format is worng. It must be list")
        elif len(coor) != 2:
            raise CustomBadRequestError(
                "Coordinate must contain only two values - [lat, lng]"
            )
        elif not all(isinstance(item, (int, float)) for item in coor):
            raise CustomBadRequestError(
                "Coordinate must contain only int or float types"
            )

        result["coordinate"] = check_coordinate_in_polygon(coor)
