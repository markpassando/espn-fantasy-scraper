import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import JSONField


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
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class League(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    league_id = models.PositiveIntegerField(
        primary_key=True, unique=True, blank=False)


class Season(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    create_date = models.DateTimeField(auto_now_add=True)
    league = models.ForeignKey(
        League,
        on_delete=models.SET_NULL,
        null=True,
        blank=False)
    year = models.PositiveIntegerField(blank=False)
    standings = JSONField(null=True, blank=True, default=None)
    last_standings_scrape = models.DateTimeField(
        null=True, blank=True, default=None)
    scores = JSONField(null=True, blank=True, default=None)
    last_scores_scrape = models.DateTimeField(
        null=True, blank=True, default=None)
    draft_recap = JSONField(null=True, blank=True, default=None)
    last_draft_recap_scrape = models.DateTimeField(
        null=True, blank=True, default=None)
    rosters = JSONField(null=True, blank=True, default=None)
    last_rosters_scrape = models.DateTimeField(
        null=True, blank=True, default=None)
    transactions = JSONField(null=True, blank=True, default=None)
    last_transaction_scrape = models.DateTimeField(
        null=True, blank=True, default=None)
