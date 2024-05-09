from django.test import TestCase
from .models import Order
from user.models import User 

class OrderModelTestCase(TestCase):
    def setUp(self):
        """테스트에 필요한 사용자 생성"""
        self.user = User.objects.create(name="test_user", email="test@example.com")

    def test_create_order(self):
        """Order 생성 테스트"""
        order = Order.objects.create(
            user=self.user,
            order_status=1,
            delivery_address="123 Street, City",
            total_price=10000,
        )

        """생성된 Order가 제대로 저장되었는지 확인"""
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.order_status, 1)
        self.assertEqual(order.delivery_address, "123 Street, City")
        self.assertEqual(order.total_price, 10000)
        self.assertEqual(order.user, self.user) 

    def test_order_str_representation(self):
        """Order 객체의 문자열 표현 확인"""
        order = Order.objects.create(
            user=self.user,
            order_status=1,
            delivery_address="123 Street, City",
            total_price=10000,
        )
        self.assertEqual(str(order), f"Order #{order.pk}")
