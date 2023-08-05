from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from .base import BaseValidator

import requests


class FacebookValidator(BaseValidator):
    def __init__(self):
        self.valid = False
        if settings.FACEBOOK_APP_ID and settings.FACEBOOK_CLIENT_SECRET:
            self.valid = True

    def validate(self, token):
        if not self.valid:
            raise ValidationError('Facebook Login Not Supported')

        if settings.TESTING:
            response = Response(status=status.HTTP_200_OK)
        else:
            response = requests.get(settings.FACEBOOK_VALIDATION_URL % (token, settings.FACEBOOK_APP_ID, settings.FACEBOOK_CLIENT_SECRET))

        return response.status_code is status.HTTP_200_OK
