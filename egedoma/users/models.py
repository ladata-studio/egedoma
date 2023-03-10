from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def _create_user(
            self, telegram_id, password, telegram_username, first_name, is_staff, is_superuser, is_active,
            last_name=None, photo=None, **extra_fields):
        if not telegram_id:
            raise ValueError('User must have a telegram account')
        if not telegram_username:
            raise ValueError('User must have a telegram username')
        if not first_name:
            raise ValueError('User must have a firstname')
        now = timezone.now()
        user = self.model(
            telegram_id=telegram_id,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            updated_at=now,
            created_at=now,
            first_name=first_name,
            last_name=last_name,
            telegram_username=telegram_username,
            photo=photo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, telegram_id, telegram_username, first_name,
            last_name=None, photo=None, **extra_fields):
        return self._create_user(
            telegram_id, None, telegram_username, first_name,
            False, False, True, last_name, photo, **extra_fields)

    def create_superuser(
            self, telegram_id, password, telegram_username,
            first_name, **extra_fields):
        return self._create_user(
            telegram_id, password, telegram_username, first_name,
            True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.IntegerField(primary_key=True, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    telegram_username = models.CharField(max_length=32, null=True, blank=True)
    photo = models.CharField(max_length=128, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'telegram_id'
    EMAIL_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['telegram_username', 'first_name']

    objects = UserManager()

    def __str__(self):
        output = f'{self.telegram_id}'
        if self.first_name:
            output += f' {self.first_name}'
        if self.last_name:
            output += f' {self.last_name}'
        return output


class AuthHash(models.Model):
    hash = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return self.hash

    class Meta:
        verbose_name_plural = "auth hashes"

