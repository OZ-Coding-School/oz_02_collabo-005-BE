from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from common.models import CommonModel


class UserManager(BaseUserManager):
    """사용자 모델 관리자로, 사용자 생성 및 관리를 처리합니다."""

    pass


class User(CommonModel, PermissionsMixin, AbstractBaseUser):
    """시스템 내 개별 사용자를 나타내는 사용자 모델입니다."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    role = models.BooleanField(default=False)
    birthday = models.CharField(max_length=15)
    # is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """사용자의 문자열 표현을 반환합니다."""
        return f"email: {self.email}, name: {self.name}"


class Adress(CommonModel):
    """사용자의 주소를 나타내는 주소 모델"""

    name = models.CharField(max_length=50)
    base = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
