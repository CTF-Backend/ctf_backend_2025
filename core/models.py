from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .creat_flag import generate_random_six_character_ascii_flag_with_letters_and_digits
from .managers import CustomUserManager, RegistrationQuestionManager


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

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class RegistrationQuestion(models.Model):
    flag = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.flag:
            self.slug = generate_random_six_character_ascii_flag_with_letters_and_digits()
        super().save(*args, **kwargs)
