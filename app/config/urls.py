"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/restaurant/", include("restaurant.urls")),
    path("api/v1/order/", include("order.urls")),
    # admin 페이지 API
    path("api/v1/admin/", include("okvadmin.urls")),

    # token 갱신
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
