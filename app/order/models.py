from django.db import models
from common.models import CommonModel
from user.models import User
from restaurant.models import Menu
from common.constants import StatusCode
from django.core.exceptions import ValidationError


# Create your models here.
class Order(CommonModel):

    ORDER_STATUS = (
        (StatusCode.PAYMENT_PENDING, "Payment pending"),
        (StatusCode.PAYMENT_SUCCESSFUL, "Payment success"),
        (StatusCode.PAYMENT_FAILED, "Payment failed"),
        (StatusCode.PAYMENT_CANCELD, "Payment cancel"),
        (StatusCode.ORDER_PENDING, "Order pending"),
        (StatusCode.ORDER_ACCEPTED, "Order accepted"),
        (StatusCode.ORDER_REJECTED, "Order rejected"),
        (StatusCode.ORDER_CANCELLED_BY_STORE, "Order cancelled by store"),
        (StatusCode.ORDER_CANCELLED_BY_CUSTOMER, "Order cancelled by customer"),
        (StatusCode.ORDER_COOKING, "Cooking"),
        (StatusCode.ORDER_COOKED, "Cooking complete"),
        (StatusCode.DELIVERY_DISPATCH_PENDING, "Delivery dispatch pending"),
        (StatusCode.DELIVERY_PICKUP_PENDING, "Delivery pickup pending"),     
        (StatusCode.DELIVERY_DELIVERING, "Delivery in progress"),            
        (StatusCode.DELIVERY_COMPLETED, "Delivery completed"),         
    )

    ORDER_CANCEL_STATUS = (
        (StatusCode.RESTAURANT_SHUT_DOWN, "Restaurant shutdown"),
        (StatusCode.RESTAURANT_PREPARE, "Restaurant prepare"),
        (StatusCode.RESTAURANT_CLOSE, "Restaurant close"),
        (StatusCode.MENU_OPTION_SOLD_OUT, "Menu option sold out"),
        (StatusCode.MENU_OPTION_HIDDEN, "Menu option hidden"),
        (StatusCode.MENU_OPTION_MODIFIED_OR_DELETED, "Menu option modified or deleted"),
        (StatusCode.ORDER_CANCELED_REASON_CUSTOMER_REQUEST, "Customer request"),
        (StatusCode.ORDER_CANCELED_REASON_WRONG_ADDRESS, "Wrong address"),
        (StatusCode.ORDER_CANCELED_REASON_RESTAURANT_ISSUE, "Restaurant issue"),
        (StatusCode.ORDER_CANCELED_REASON_OUT_OF_STOCK, "Out of stock"),
        (StatusCode.ORDER_CANCELED_REASON_CLOSED, "Closed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.PositiveIntegerField(choices=ORDER_STATUS, default=StatusCode.PAYMENT_PENDING)
    cooking_time = models.DateTimeField(null=True)
    delivery_address = models.CharField(max_length=255)
    store_request = models.TextField(null=True, default=None)
    rider_request = models.TextField(null=True, default=None)
    total_price = models.PositiveIntegerField(null=True, default=None)
    order_time = models.DateTimeField(auto_now_add=True)
    cancle_reason = models.PositiveIntegerField(choices=ORDER_CANCEL_STATUS, null=True, default=None)
    order_price = models.PositiveBigIntegerField(null=True, default=0)
    delivery_fee = models.PositiveSmallIntegerField(null=True, default=0)
    def clean(self):
        # total_price 필드에 대한 음수 값 확인
        if self.total_price < 0:
            raise ValidationError("Total price cannot be negative.")

    def create_order(
        cls,
        user,
        delivery_address,
        total_price,
        order_status=StatusCode.ORDER_PENDING,
        store_request=None,
        rider_request=None,
        cancel_reason=None,
    ):
        """
        사용자, 배송 주소, 총 가격을 기반으로 주문을 생성
        기본적으로 order_status는 주문 확인중으로 설정
        """
        order = cls(
            user=user,
            order_status=order_status,
            delivery_address=delivery_address,
            store_request=store_request,
            rider_request=rider_request,
            total_price=total_price,
            cancel_reason=cancel_reason,
        )
        order.save()
        return order

    def __str__(self):
        return f"Order #{self.id}"


class Order_detail(CommonModel):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_name"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order Detail - Order #{self.order_id}, Menu: {self.menu.name}, Quantity: {self.quantity}"


class Order_option(CommonModel):

    order_detail = models.ForeignKey(Order_detail, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=255)
    option_price = models.PositiveIntegerField(null=True, default=None)
    option_group_name = models.CharField(max_length=50)

    def __str__(self):
        return f"Order Option - Group: {self.order_detail.option_group_name}, Name: {self.option_name}, Price: {self.option_price}"


class Payment(CommonModel):

    PAYMENT_STATUS = (
        (StatusCode.PAYMENT_PENDING, "Payment pending"),
        (StatusCode.PAYMENT_SUCCESSFUL, "Payment successful"),
        (StatusCode.PAYMENT_FAILED, "Payment failed"),
        (StatusCode.PAYMENT_CANCELD, "Payment cancelled"),
        (StatusCode.PAYMENT_OFFLINE, "Payment offline"),
    )

    METHOD_STATUS = (
        (StatusCode.PAYMENT_ONLINE_CARD, "Online - card"),
        (StatusCode.PAYMENT_ONLINE_CASH, "Online - cash"),
        (StatusCode.PAYMENT_OFFLINE_CARD, "Offline - card"),
        (StatusCode.PAYMENT_OFFLINE_CASH, "Offline - cash"),
    )

    FAILURE_REASON_STATUS = (
        (StatusCode.PAYMENT_INVALID_CARD_INFO, "Invalid card info"),
        (StatusCode.PAYMENT_INSUFFICIENT_BALANCE, "Insufficient balance"),
        (StatusCode.PAYMENT_SERVER_INTERNAL_ERROR, "Server internal error"),
        (StatusCode.PAYMENT_COMMUNICATION_ERROR, "Communication error"),
        (StatusCode.PAYMENT_ORDER_CANCELD, "Order cancelled"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.PositiveIntegerField(choices=METHOD_STATUS)
    status = models.PositiveIntegerField(choices=PAYMENT_STATUS, default=StatusCode.PAYMENT_PENDING)
    cancle_reason = models.PositiveIntegerField(choices=FAILURE_REASON_STATUS, null=True, default=None)
    order_price = models.PositiveIntegerField(null=True, default=None)
    delivery_fee = models.PositiveIntegerField(null=True, default=None)
    total_price = models.PositiveIntegerField(null=True, default=None)

    def clean(self):
        # total_price 필드에 대한 음수 값 확인
        if self.total_price < 0:
            raise ValidationError("Total price cannot be negative.")

        # delivery_fee 필드에 대한 음수 값 확인
        if self.delivery_fee < 0:
            raise ValidationError("Delivery fee amount cannot be negative.")

        # order_price 필드에 대한 음수 값 확인
        if self.order_price < 0:
            raise ValidationError("Order price cannot be negative.")

    def __str__(self):
        return f"Payment - Order: {self.order}, Method: {self.method}, Status: {self.status}"


class Delivery_man(CommonModel):

    delivery_man_name = models.CharField(max_length=255)
    delivery_type = models.IntegerField()

    def __str__(self):
        return self.delivery_man_name


class Delivery(CommonModel):

    DELIVERY_STATUS = (
        (StatusCode.DELIVERY_DISPATCH_PENDING, "Dispatch pending"),
        (StatusCode.DELIVERY_PICKUP_PENDING, "Pickup pending"),
        (StatusCode.DELIVERY_DELIVERING, "Delivering"),
        (StatusCode.DELIVERY_COMPLETED, "Completed"),
    )

    delivery_man = models.ForeignKey(
        Delivery_man, on_delete=models.CASCADE, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    estimated_time = models.DateTimeField(null=True, default=None)
    completion_time = models.DateTimeField(null=True, default=None)
    is_self_delivery = models.BooleanField(default=0)
    delivery_status = models.PositiveIntegerField(choices=DELIVERY_STATUS, null=True, default=StatusCode.DELIVERY_DISPATCH_PENDING)
    cancle_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"Delivery - Order: {self.order}, Delivery Man: {self.delivery_man}, Estimated Time: {self.estimated_time}, Completion Time: {self.completion_time}"


class Delivery_fee_info(CommonModel):
    name = models.CharField(max_length=20)
    delivery_fee = models.PositiveIntegerField(null=True, default=None)
    code = models.CharField(max_length=20)
    status = models.BooleanField(default=0)

    def __str__(self):
        return self.name
