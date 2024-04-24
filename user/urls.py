from django.urls import path
from .views import *

# api/v1/user/
urlpatterns = [
    # api/v1/user/create/
    path('create/', UserCreateView.as_view(), name='user-create'),
    # api/v1/user/check?email=test@naver.com
    path('check/', EmailCheckView.as_view(), name='user-email-check'),
]