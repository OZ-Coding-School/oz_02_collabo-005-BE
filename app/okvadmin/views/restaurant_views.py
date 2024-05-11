from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..services.restaurant_services import RestaurantListService
from common.utils.response_formatter import JSONDataFormatter

from pprint import pp


class RestaurantListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # staff가 아니면 권한이 없음
        if not request.user.is_staff:
            return Response({"code": 403, "message": "you are not staff"}, status=403)

        return RestaurantListService().response()
