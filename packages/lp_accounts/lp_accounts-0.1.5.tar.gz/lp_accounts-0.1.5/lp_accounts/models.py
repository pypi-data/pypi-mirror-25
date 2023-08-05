from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    TYPE_DEFAULT = 1
    TYPE_GOOGLE = 2
    TYPE_FACEBOOK = 3
    TYPES = (
        (TYPE_DEFAULT, 'Default'),
        (TYPE_GOOGLE, 'Google'),
        (TYPE_FACEBOOK, 'Facebook')
    )

    type = models.IntegerField(choices=TYPES, default=TYPE_DEFAULT)

    def __str__(self):
        return self.username
