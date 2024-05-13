from django.db import models
from common.models import CommonModel
from user.models import User
from restaurant.models import Menu
from django.core.exceptions import ValidationError


# Create your models here.
class Order(CommonModel):

    STATUS_CHOICES = (
        (0, "Order received"),
        (1, "Cooking"),
        (2, "Cooking complete"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.PositiveIntegerField(choices=STATUS_CHOICES)
    cooking_time = models.DateTimeField(auto_now_add=True, null=True)
    delivery_address = models.CharField(max_length=255)
    dispatch_status = models.IntegerField(null=True, default=None)
    store_request = models.TextField(null=True, default=None)
    rider_request = models.TextField(null=True, default=None)
    total_price = models.PositiveIntegerField(null=True, default=None)
    order_time = models.DateTimeField(auto_now_add=True)
    cancle_reason = models.TextField(null=True, default=None)
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
        order_status=0,
        dispatch_status=None,
        store_request=None,
        rider_request=None,
        cancel_reason=None,
    ):
        """
        사용자, 배송 주소, 총 가격을 기반으로 주문을 생성
        기본적으로 order_status는 0(주문 접수됨)로 설정
        """
        order = cls(
            user=user,
            order_status=order_status,
            delivery_address=delivery_address,
            dispatch_status=dispatch_status,
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
    option_group_name = models.CharField(max_length=30)

    def __str__(self):
        return f"Order Option - Group: {self.Order_detail.order_group_name}, Name: {self.option_name}, Price: {self.option_price}"


class Payment(CommonModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    payment_time = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(null=True, default=None)
    coupon = models.PositiveIntegerField(null=True, default=None)
    delivery_pay = models.PositiveIntegerField(null=True, default=None)
    final_price = models.PositiveIntegerField(null=True, default=None)

    def clean(self):
        # total_price 필드에 대한 음수 값 확인
        if self.total_price < 0:
            raise ValidationError("Total price cannot be negative.")

        # coupon 필드에 대한 음수 값 확인
        if self.coupon < 0:
            raise ValidationError("Coupon amount cannot be negative.")

        # delivery_pay 필드에 대한 음수 값 확인
        if self.delivery_pay < 0:
            raise ValidationError("Delivery pay amount cannot be negative.")

        # final_price 필드에 대한 음수 값 확인
        if self.final_price < 0:
            raise ValidationError("Final price cannot be negative.")

    def __str__(self):
        return f"Payment - Order: {self.order}, Method: {self.payment_method}, Time: {self.payment_time}"


class Delivery_man(CommonModel):

    delivery_man_name = models.CharField(max_length=255)
    delivery_type = models.IntegerField()

    def __str__(self):
        return self.delivery_man_name


class Delivery(CommonModel):

    delivery_man = models.ForeignKey(Delivery_man, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    estimated_time = models.DateTimeField()
    completion_time = models.DateTimeField()

    def __str__(self):
        return f"Delivery - Order: {self.order}, Delivery Man: {self.delivery_man}, Estimated Time: {self.estimated_time}, Completion Time: {self.completion_time}"
