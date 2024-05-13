from django.urls import path
from .views import *

# api/v1/user/
urlpatterns = [
    # api/v1/user/
    path("", UserView.as_view(), name="user"),
    # api/v1/user/login/
    path("login/", LoginView.as_view(), name="user-login"),
    # api/v1/user/logout/
    path("logout/", LogoutView.as_view(), name="user-logout"),
    # api/v1/user/update/
    path("update/", UpdateView.as_view(), name="user-update"),
    # api/v1/user/delete/
    path("delete/", DeleteView.as_view(), name="user-delete"),
    # api/v1/user/check?email=test@naver.com
    path("check/", EmailCheckView.as_view(), name="user-email-check"),
    # api/v1/user/address/
    path("address/", AddressView.as_view(), name="user-address"),
    # api/v1/user/address/update/
    path("address/update/", AddressUpdateView.as_view(), name="user-address-update"),
    # api/v1/user/address/check-coordinate/
    path("address/check-coordinate/", AddressCoordinateWithinPolygonView.as_view(), name="user-address-check-coordinate")
]
