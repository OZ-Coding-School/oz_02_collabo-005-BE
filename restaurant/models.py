from django.db import models
from common.models import CommonModel

class RestaurantManager(models.Manager):
    """레스토랑 모델 관리자로, 레스토랑 생성을 처리합니다."""

    def create_restaurant(self, name, representative_menu, representative_menu_picture, description, notice, delivery_fee, minimum_order_amount, opening_time, closing_time, status):
        """이름, 대표 메뉴, 대표 메뉴 사진, 설명, 공지, 배달비, 최소 주문 금액, 오픈 시간, 닫는 시간, 상태를 사용하여 새로운 레스토랑을 생성하고 반환합니다."""

        restaurant = self.model(
            name=name,
            representative_menu=representative_menu,
            representative_menu_picture=representative_menu_picture,
            description=description,
            notice=notice,
            delivery_fee=delivery_fee,
            minimum_order_amount=minimum_order_amount,
            opening_time=opening_time,
            closing_time=closing_time,
            status=status
        )
        restaurant.save(using=self._db)

        return restaurant
class Restaurant(CommonModel):

    STATUS_CHOICES = (
        (1, "Open"),
        (2, "Closed"),
        (3, "Under Maintenance"),
    )

    name = models.CharField(max_length=50)
    representative_menu = models.PositiveIntegerField(null=True, default=None)
    representative_menu_picture = models.URLField(null=True, default=None)
    description = models.TextField(null=True, default=None)
    notice = models.TextField(null=True, default=None)
    delivery_fee = models.PositiveIntegerField(null=True, default=None)
    minimum_order_amount = models.PositiveIntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return f"({self.id}){self.name}"


"""Hashtag model"""


class Hashtag(CommonModel):
    hashtag = models.CharField(max_length=20)

    def __str__(self):
        return self.hashtag


class RestaurantHashtag(CommonModel):
    """hashtags는 역참조를 하기 위한 역할"""

    restaurant = models.ForeignKey(
        Restaurant, related_name="hashtags", on_delete=models.CASCADE
    )
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.restaurant} - {self.hashtag}"


"""Category model"""


class Category(CommonModel):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category


class RestaurantCategory(CommonModel):
    """categories는 역참조를 하기 위한 역할"""

    restaurant = models.ForeignKey(
        Restaurant, related_name="categories", on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.restaurant} - {self.category}"


"""Menu model"""


class Menu_group(CommonModel):

    restaurant = models.ForeignKey(
        Restaurant, related_name="menu_groups", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)


class Menu(CommonModel):

    STATUS_CHOICES = (
        (1, "Open"),
        (2, "Sold Out"),
        (3, "Hidden"),
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_group = models.ForeignKey(Menu_group, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.URLField(null=True, default=None)
    description = models.CharField(max_length=255, null=True, default=None)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Option_group(CommonModel):

    STATUS_CHOICES = (
        (1, "Single"),
        (2, "Multiple"),
    )

    mandatory = models.BooleanField(default=False)
    choice_mode = models.IntegerField(choices=STATUS_CHOICES, default=2)
    maximum = models.IntegerField()


class Option_group_to_menu(CommonModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    option_group = models.ForeignKey(Option_group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.menu} - {self.option_group}"


class Option(CommonModel):
    option_group = models.ForeignKey(Option_group, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.name
