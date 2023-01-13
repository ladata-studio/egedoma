from django.db import models
from django.utils import timezone


class AuthHash(models.Model):
    hash = models.CharField(max_length=64)
    created = models.DateTimeField(editable=False, default=timezone.now())
    is_expired = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return self.hash

    class Meta:
        verbose_name_plural = "auth hashes"


class Student(models.Model):
    telegram_id = models.IntegerField(unique=True)
    created = models.DateTimeField(editable=False, default=timezone.now())
    is_active = models.BooleanField(editable=False, default=False)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    telegram_username = models.CharField(max_length=32, null=True, blank=True)
    photo = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        output = f'{self.telegram_id}'
        if self.first_name:
            output += f' {self.first_name}'
        if self.last_name:
            output += f' {self.last_name}'
        return output

