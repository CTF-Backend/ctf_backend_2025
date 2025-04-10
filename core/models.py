from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    payed = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Authority(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    authority = models.CharField(max_length=256)
    verified = models.BooleanField(default=False)

    def __str__(self):

        return f"{'✔️' if self.verified else '❌'}{self.user}:{self.authority}"
