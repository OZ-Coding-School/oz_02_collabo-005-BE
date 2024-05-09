from django.urls import path
from .views import *

# api/v1/order/
urlpatterns = [
    # api/v1/order/
    path("", OrderCreateView.as_view(), name="order-create"),
    # api/v1/order/list/
    path("list/", OrderGetListView.as_view(), name="order-get-list"),
]
