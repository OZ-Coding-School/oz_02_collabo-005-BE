from django.urls import path
from .views import *

# api/v1/restaurant/
urlpatterns = [
    # api/v1/restaurant/list/
    path("list/", RestaurantGetListView.as_view(), name="restaurant-list"),
    # api/v1/restaurant/menu
    path("menu/status/", MenuStatusView.as_view(), name="menu-status"),
    # api/v1/restaurant/menu/list?restaurantId=1
    path("menu/list", RestaurantGetDetailView.as_view(), name="restaurant-detail"),
    # api/v1/restaurant/option/list?menuId=1
    path("option/list", MenuGetDetailView.as_view(), name="menu-option-detail"),
]
