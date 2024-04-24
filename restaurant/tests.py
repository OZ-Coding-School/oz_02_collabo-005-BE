from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import success, error
from .models import (
    Restaurant,
    Hashtag,
    RestaurantHashtag,
    Category,
    RestaurantCategory,
    Menu_group,
    Menu,
    Option_group,
    Option_group_to_menu,
    Option,
)
from django.utils import timezone


class RestaurantTestCase(TestCase):
    def test_create_restaurant(self):
        # Create a restaurant
        restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            representative_menu=1,
            representative_menu_picture="http://example.com/image.jpg",
            description="Test description",
            notice="Test notice",
            delivery_fee=10,
            minimum_order_amount=20,
            opening_time=timezone.now(),
            closing_time=timezone.now(),
            status=1,
        )

        # Check if the restaurant is created
        self.assertEqual(restaurant.name, "Test Restaurant")
        self.assertEqual(restaurant.description, "Test description")
        self.assertEqual(restaurant.status, 1)


class UserTestCase(TestCase):
    def test_create_user(self):
        # Create a user
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        # Check if the user is created
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")


class MessagesTestCase(TestCase):
    def test_messages(self):
        # Create a request with message middleware
        factory = RequestFactory()
        request = factory.get("/")
        storage = FallbackStorage(request)
        request.session = storage

        # Add messages to the request
        success(request, "Test success message")
        error(request, "Test error message")

        # Get messages from the request
        messages = get_messages(request)

        # Check if the messages are added
        self.assertEqual(
            [msg.message for msg in messages],
            ["Test success message", "Test error message"],
        )
