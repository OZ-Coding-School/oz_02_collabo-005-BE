from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from common.models import CommonModel


class UserManager(BaseUserManager):
    """사용자 모델 관리자로, 사용자 생성 및 관리를 처리합니다."""

    def create_user(
        self, email, password, name, phone_number, birthday=None, **extra_fields
    ):
        """이메일, 비밀번호 및 추가 필드를 사용하여 새로운 사용자를 생성하고 반환합니다.

        이메일이 제공되지 않을 경우 ValueError를 발생시킵니다.
        """
        if not email:
            raise ValueError("사용자는 이메일 주소를 가져야 합니다")
        if not password:
            raise ValueError("사용자는 패스워드를 가져야 합니다")
        if not name:
            raise ValueError("사용자는 이름를 가져야 합니다")
        if not phone_number:
            raise ValueError("사용자는 휴대폰 번호를 가져야 합니다")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            birthday=birthday,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name, phone_number, birthday=None):

        user = self.create_user(email, password, name, phone_number, birthday)
        user.is_superuser = True
        user.is_staff = True  # Assuming role field represents the user's role
        user.save(using=self._db)
        return user


class User(CommonModel, PermissionsMixin, AbstractBaseUser):
    """시스템 내 개별 사용자를 나타내는 사용자 모델입니다."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    birthday = models.CharField(max_length=15, default=None, null=True)
    # is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """사용자의 문자열 표현을 반환합니다."""
        return f"email: {self.email}, name: {self.name}"


class Address(CommonModel):
    """사용자의 주소를 나타내는 주소 모델"""

    name = models.CharField(max_length=50)
    base = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
