from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
  def create_user(self, email, name, password=None):
    if not email:
      raise ValueError("Email is required")

    email = self.normalize_email(email)
    user = self.model(email=email, name=name)

    user.set_password(password)
    user.save(using=self._db)

    return user

    def create_superuser(self, email, name, password):
      user = self.create_user(email, name, password)
      user.is_superuser = True

      user.save(using=self._db)

      return user

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

  def __str__(self):
    return self.email