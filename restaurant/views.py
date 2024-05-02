from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *


class RestaurantGetListView(APIView):
    """
    토큰 인증 후,
    Main 화면에 나타나는 레스토랑 사진, 이름, 해쉬태그, 카테고리 등 정보를 가져오는 API
    각 다른 테이블에서 데이터를 가져온다(restaurant, hashtag, category)
    """

    def get(self, request):
        # 토큰 인증
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:

            restaurant_detail = request.GET.get("id", None)
            # Restaurant 테이블에서 id, name, picture값을 가져온다
            restaurants = Restaurant.objects.all().values(
                "id",
                "name",
                "description",
                "delivery_fee",
                "representative_menu_picture",
            )

            # for restaurant in restaurants에서 빠져나온 값 들을 하나씩 List 형태로 저장한다.
            response_data = []

            for restaurant in restaurants:
                # hashtag, category는 한 번 돌면 새로운 List를 만든다.
                hashtag_list = []
                category_list = []

                # 각자의 Class에서 restaurant의 id 값을 가져오고,
                # restaurants에서 가져온 id 값과 같은 데이터에 id 값들을 저장 (hashtag_ids, category_ids)
                hashtag_ids = RestaurantHashtag.objects.filter(
                    restaurant=restaurant["id"]
                ).values("hashtag_id")
                category_ids = RestaurantCategory.objects.filter(
                    restaurant=restaurant["id"]
                ).values("category_id")

                # id 값을 가지고 hashtag와 category의 value를 가져옴
                # for문을 통해서 각 컬럼 개수만큼 반복
                for hashtag in hashtag_ids:
                    id = hashtag["hashtag_id"]
                    hashtag_value = Hashtag.objects.filter(id=id).values("hashtag")
                    hashtag_list.append(hashtag_value)

                for category in category_ids:
                    id = category["category_id"]
                    category_value = Category.objects.filter(id=id).values("category")
                    category_list.append(category_value)

                # 각 테이블에서 가져온 컬럼 값들을 res에 저장하고 Response
                # hashtag나 category 값이 없으면 빈 리스트로 표시
                res = {
                    "id": restaurant["id"],
                    "name": restaurant["name"],
                    "image": restaurant["representative_menu_picture"],
                    "hashtag": hashtag_list,
                    "category": category_list,
                }
                response_data.append(res)
                stat = status.HTTP_200_OK
            return Response(response_data, stat)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RestaurantGetDetailView(APIView):
    def get(self, request):
        # 토큰 인증
        JWT_authenticator = JWTAuthentication()
        is_validated_token = JWT_authenticator.authenticate(request)

        if is_validated_token:
            restaurant_id = request.GET.get("restaurantId")  # restaurantId를 받아옴

            # get요청으로 restaurant_id을 받아옴
            # restaurant_id가 있다면 try 없으면 except(예외 처리)
            if restaurant_id:
                try:
                    restaurant = Restaurant.objects.get(id=restaurant_id)
                except Restaurant.DoesNotExist:
                    return Response(
                        {"error": "Restaurant not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                response_data = []  # 전체 데이터
                menu_group_list = []

                # Restaurant_id 가 같은 Menu_group_id를 가져온다
                menu_group_ids = Menu_group.objects.filter(
                    restaurant=restaurant.id
                ).values("id")

                for menu_group in menu_group_ids:
                    menu_list = []

                    menu_group_id = menu_group["id"]

                    # Menu_group에서 description의 값들을 가져온다.
                    menu_group_value = (
                        Menu_group.objects.filter(id=menu_group_id)
                        .values("description")
                        .first()
                    )
                    # description이라는 컬럼이 있는 데이터들의 값만 가져온다
                    if menu_group_value:
                        # 컬럼 형식에서 description의 내용만 가져온다.
                        menu_group_description = menu_group_value["description"]

                        # Menu_group과 같은 방식으로 Menu의 컬럼들의 데이터를 가져온다.
                        # Menu_group_id와 같은 Menu_id를 가지고 있는 데이터들을 queryset으로 나눈다.
                        menus = Menu.objects.filter(menu_group=menu_group_id).values(
                            "id", "picture", "name", "price", "description"
                        )

                        # menus에서 가져온 데이터를 하나씩 menu_list에 추가한다
                        for menu in menus:
                            menu_list.append(menu)
                        # Menu_group에 description 데이터를 가져오고 Menu에서 가져온 각 데이터들을
                        # menu_group_data에 튜플 형태로 넣어준다.
                        menu_group_data = {
                            "description": menu_group_description,
                            "menus": menu_list,
                        }
                        menu_group_list.append(menu_group_data)

                res = {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "image": restaurant.representative_menu_picture,
                    "description": restaurant.description,
                    "delivery_fee": restaurant.delivery_fee,
                    "menu_group_list": menu_group_list,
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "restaurantId parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
