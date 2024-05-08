from django.urls import path
from .views import *

# api/v1/order/
urlpatterns = [
    # api/v1/order/
    path("", TestView.as_view(), name="order-create"),
]
