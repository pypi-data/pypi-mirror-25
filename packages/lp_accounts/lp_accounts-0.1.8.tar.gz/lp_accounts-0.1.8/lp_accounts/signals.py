from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, created, raw, **kwargs):
    if settings.CONFIRM_EMAIL_ENABLED and created and not raw:
        mail.send_mail(
            settings.CONFIRM_EMAIL_SUBJECT, settings.CONFIRM_EMAIL_BODY,
            settings.CONFIRM_EMAIL_SENDER, [instance.email],
            fail_silently=False,
        )