from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .exceptions import *


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        email = extra_fields.get('email')
        if email:
            self.email_validator(email)
        if not username:
            raise UsernameIsRequired()

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    @classmethod
    def email_validator(cls, email):
        validate_email(email)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        user = self.create_user(username, password, **extra_fields)
        user.save(using=self._db)
        return user
