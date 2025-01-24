from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .exceptions import *


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise UsernameIsRequired()
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # @classmethod
    # def email_validator(cls, email):
    #     try:
    #         validate_email(email)
    #     except ValidationError:
    #         raise EmailISNotValid()
    #
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise IsSuperuserMustBeTrue()
        user = self.create_user(username, password, **extra_fields)
        user.save(using=self._db)
        return user
