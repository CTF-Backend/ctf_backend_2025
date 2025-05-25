from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.db import models

from .creat_flag import generate_random_six_character_ascii_flag_with_letters_and_digits
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


class RegistrationQuestionManager(models.Manager):
    def create_article(self, *args, **kwargs):
        flag = generate_random_six_character_ascii_flag_with_letters_and_digits()
        return self.create(*args, **kwargs, flag=flag)
