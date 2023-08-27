from django.db.models import *
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = EmailField('email address', unique=True)
    password = CharField(max_length=255, null=False, blank=False)

    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    is_Seller = BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class Seller(MyUser):
    name = CharField(max_length=255, null=False, blank=False)
    second_name = CharField(max_length=255, null=False, blank=False)
    phone_number = CharField(max_length=255, null=False, blank=False)
    description = CharField(max_length=255, null=True, blank=True)


class Customer(MyUser):
    name = CharField(max_length=255, null=False, blank=False)
    second_name = CharField(max_length=255, null=False, blank=False)
    phone_number = CharField(max_length=255, null=False, blank=False)
    card_number = CharField(max_length=255, null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    post_code = CharField(max_length=255, null=True, blank=True)







