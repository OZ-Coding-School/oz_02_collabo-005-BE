from django.urls import path
from .views import *

# api/v1/user/
urlpatterns = [
    # api/v1/user/create/
    path("", UserCreateView.as_view(), name="user-create"),
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
]
