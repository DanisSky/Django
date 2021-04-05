from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="account")
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
