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
    path("order/list/", ov.OrderGetListView.as_view(), name="admin-order-list"),
    # order/approve/
    path("order/approve/", ov.OrderApprove.as_view(), name= "admin-order-approve"),
    # order/cancle/
    path("order/cancle/", ov.OrderCancleView.as_view(), name= "admin-order-cancle"),
    # order/cooking/
    path("order/cooking/", ov.OrderCooking.as_view(), name= "admin-order-cooking"),
    # order/cooked/
    path("order/cooked/", ov.OrderCooked.as_view(), name= "admin-order-cooked"),
    # order/assign/
    path("order/assign/", ov.AssignDelivery.as_view(), name= "admin-order-assign"),
    # order/delivering/
    path("order/delivering/", ov.OrderDelivering.as_view(), name= "admin-order-delivering"),
    # order/completedelivery/
    path("order/completedelivery/", ov.CompleteDelivery.as_view(), name= "admin-order-completedelivery"),

    # 테스트용 API
    # api/v1/admin/test/
    path("test/", tv.TestView.as_view(), name="admin-test"),
]
