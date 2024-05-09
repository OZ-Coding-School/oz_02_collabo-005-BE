from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from .models import User, Address


class CustomUserManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()
        email = "test@example.com"
        password = "testpassword"
        name = "Test User"
        phone_number = "123-456-7890"
        birthday = "1990-01-01"

        # 이메일 없이 사용자 생성 시 ValueError가 발생하는지 확인
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                password=password,
                name=name,
                phone_number=phone_number,
                birthday=birthday,
            )

        # 패스워드 없이 사용자 생성 시 ValueError가 발생하는지 확인
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=email,
                password=None,
                name=name,
                phone_number=phone_number,
                birthday=birthday,
            )

        # 이름 없이 사용자 생성 시 ValueError가 발생하는지 확인
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=email,
                password=password,
                name=None,
                phone_number=phone_number,
                birthday=birthday,
            )

        # 휴대폰 번호 없이 사용자 생성 시 ValueError가 발생하는지 확인
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=email,
                password=password,
                name=name,
                phone_number=None,
                birthday=birthday,
            )

        # 모든 필수 정보가 제공되면 정상적으로 사용자가 생성되는지 확인
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            birthday=birthday,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.birthday, birthday)


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_superuser(self):
        user = self.User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            name="Admin User",
            phone_number="1234567890",
            birthday="1990-01-01",
        )

        self.assertTrue(user.pk)
        self.assertTrue(user.is_superuser)

        self.assertEqual(user.is_staff, 1)


class AddressTestCase(TestCase):
    def setUp(self):
        """사용자 생성"""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password",
            name="John Doe",
            phone_number="1234567890",
            birthday="1990-01-01",
        )

        """주소 생성"""
        self.address = Address.objects.create(
            user=self.user, base="123 Street", detail="Apt 101", name="Home"
        )

    def test_address_created(self):
        """주소가 정상적으로 생성되었는지 확인"""
        self.assertEqual(Address.objects.count(), 1)
        saved_address = Address.objects.first()
        self.assertEqual(saved_address.user, self.user)
        self.assertEqual(saved_address.base, "123 Street")
        self.assertEqual(saved_address.detail, "Apt 101")
        self.assertEqual(saved_address.name, "Home")

    def test_unique_address_name_per_user(self):
        """동일한 사용자에 대해 중복된 이름의 주소 생성 시도"""
        with self.assertRaises(Exception):
            Address.objects.create(
                user=self.user,
                base="456 Avenue",
                detail="Unit 202",
                name="Home" """같은 이름으로 생성""",
            )
