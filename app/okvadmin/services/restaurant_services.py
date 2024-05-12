from rest_framework.response import Response
from common.utils.response_formatter import JSONDataFormatter

from restaurant.models import Restaurant
from okvadmin.serializers.restaurant_serializers import RestaurantListSerializer


class RestaurantListService:
    def get(self):
        return Restaurant.objects.values("id", "name")

    def response(self):
        response = Response()
        res_formatter = JSONDataFormatter()
        
        # 데이터 가져와서 formatter에 담기
        res_formatter.add_response_data({"restaurants": self.get()})
        res_formatter.message = "Select restaurant list success"
        response.data = res_formatter.get_response_data()
        response.status_code = res_formatter.status
        return response
