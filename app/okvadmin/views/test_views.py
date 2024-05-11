from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.auth_services import AdminLoginService
from common.utils.response_formatter import JSONDataFormatter

from pprint import pp


class TestView(APIView):
    def get(self, request):
        res_formatter = JSONDataFormatter(200)
        response = Response()

        res_formatter.message = "test in"
        res_formatter.add_response_data({"is_staff": request.user.is_staff})
        response.data = res_formatter.get_response_data()
        response.status_code = res_formatter.status
        return response
