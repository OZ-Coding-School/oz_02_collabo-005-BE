from django.test import TestCase
from django.contrib.auth import get_user_model


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
        # Create a superuser
        user = self.User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            name='Admin User',
            phone_number='1234567890',
            birthday='1990-01-01'
        )

        # Check if the user is created and is_superuser is True
        self.assertTrue(user.pk)
        self.assertTrue(user.is_superuser)

        # Check if the user's role is set properly
        self.assertEqual(user.is_staff, 1)