from django.urls import path
from .views import *

# api/v1/restaurant/
urlpatterns = [
    # api/v1/restaurant/list/
    path("list/", RestaurantGetListView.as_view(), name="restaurant-list"),
]
