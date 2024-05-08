from django.urls import path
from .views import auth_views as av

# api/v1/user/
urlpatterns = [
    # api/v1/admin/auth
    path("auth", av.AdminLoginView.as_view(), name="admin-auth"),
]
