from django.test import TestCase
from .models import Restaurant
import datetime


class RestaurantModelTestCase(TestCase):
    def test_create_restaurant(self):
        name = "Test Restaurant"
        representative_menu = 1
        representative_menu_picture = "http://example.com/menu.jpg"
        logo = "http://example.com/logo.jpg"
        description = "This is a test restaurant."
        notice = "Test notice."
        delivery_fee = 5000
        minimum_order_amount = 20000
        opening_time = datetime.time(9, 0, 0)
        closing_time = datetime.time(21, 0, 0)
        status = 1

        restaurant = Restaurant.objects.create(
            id=1,
            name=name,
            representative_menu=representative_menu,
            representative_menu_picture=representative_menu_picture,
            logo=logo,
            description=description,
            notice=notice,
            delivery_fee=delivery_fee,
            minimum_order_amount=minimum_order_amount,
            opening_time=opening_time,
            closing_time=closing_time,
            status=status,
        )

        """생성된 레스토랑의 필드가 예상대로 설정되었는지 확인"""
        self.assertEqual(restaurant.name, name)
        self.assertEqual(restaurant.representative_menu, representative_menu)
        self.assertEqual(
            restaurant.representative_menu_picture, representative_menu_picture
        )
        self.assertEqual(restaurant.logo, logo)
        self.assertEqual(restaurant.description, description)
        self.assertEqual(restaurant.notice, notice)
        self.assertEqual(restaurant.delivery_fee, delivery_fee)
        self.assertEqual(restaurant.minimum_order_amount, minimum_order_amount)
        self.assertEqual(restaurant.opening_time, opening_time)
        self.assertEqual(restaurant.closing_time, closing_time)
        self.assertEqual(restaurant.status, status)

    def test_string_representation(self):

        restaurant = Restaurant.objects.create(
            id=1,
            name="Test Restaurant",
            representative_menu=1,
            representative_menu_picture="http://example.com/menu.jpg",
            logo="http://example.com/logo.jpg",
            description="This is a test restaurant.",
            notice="Test notice.",
            delivery_fee=5000,
            minimum_order_amount=20000,
            opening_time=datetime.time(9, 0, 0),
            closing_time=datetime.time(21, 0, 0),
            status=1,
        )
        self.assertEqual(str(restaurant), "(1)Test Restaurant")
