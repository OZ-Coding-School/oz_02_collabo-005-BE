from django.urls import path
from .views import *

# api/v1/order/
urlpatterns = [
    # api/v1/order/
    path("", OrderCreateView.as_view(), name="order-create"),
    # api/v1/order/list/
    path("list/", OrderListView.as_view(), name="order-list"),
    # api/v1/order/detail?id=123
    path("detail", OrderDetailView.as_view(), name="order-detale"),

    path("cart/check/", CartCheckView.as_view(), name="order-check-cart")
]
