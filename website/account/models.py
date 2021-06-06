import uuid

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from account.task import send_verification_email


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(_('verified'), default=False)
    verification_uuid = models.UUIDField(_('Unique Verification UUID'), default=uuid.uuid4)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True)

    def __str__(self):
        return self.user.get_full_name()

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
        instance.account.save()

    @receiver(post_save, sender=User)
    def user_post_save(sender, instance, **kwargs):
        instance = Account.objects.get(user=instance)
        if not instance.is_verified:
            # Send verification email
            send_verification_email.delay(instance.user_id, instance.verification_uuid)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
