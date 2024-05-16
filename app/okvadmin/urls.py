from django.urls import path
from .views import auth_views as av, test_views as tv, restaurant_views as rv, order_views as ov 

urlpatterns = [
    ### base: api/v1/admin/ ###

    # auth/
    path("auth/", av.AdminLoginView.as_view(), name="admin-auth"),

    ### restaurant ###
    # restaurant/list
    path("restaurant/list/", rv.RestaurantListView.as_view(), name="admin-restaurant-list"),
    
    ### order ###
    # order/list/
    path("order/list/", ov.OrderTestView.as_view(), name="admin-order-list"),
    path("order/approve/", ov.OrderApprove.as_view(), name= "admin-order-approve"),

    # 테스트용 API
    # api/v1/admin/test/
    path("test/", tv.TestView.as_view(), name="admin-test"),
]
