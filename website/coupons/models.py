from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    code = models.CharField(_('code'), max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(_('discount'), validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(_('active'))

    def __str__(self):
        return self.code
