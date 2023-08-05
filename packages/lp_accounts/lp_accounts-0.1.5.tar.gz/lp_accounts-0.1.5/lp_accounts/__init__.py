from django.conf import settings
import sys

# Flag for Testing Environment
settings.TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Extend Native User Model
settings.AUTH_USER_MODEL = 'lp_accounts.User'

# REST Framework Configuration
settings.REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   )
}

# Reset Password Email Configuration
settings.RESET_PASSWORD_SENDER = getattr(settings, 'RESET_PASSWORD_SENDER', 'support@launchpeer.com')
settings.RESET_PASSWORD_SUBJECT = getattr(settings, 'RESET_PASSWORD_SUBJECT', 'Reset Password Request')

# Google Sign-In Integration
# https://developers.google.com/identity/sign-in/web/backend-auth
settings.GOOGLE_APP_ID = getattr(settings, 'GOOGLE_APP_ID', None)
settings.GOOGLE_VALIDATION_URL = getattr(settings, 'GOOGLE_VALIDATION_URL', 'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=%s')

# Facebook Login Integration
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#checktoken
settings.FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', None)
settings.FACEBOOK_CLIENT_SECRET = getattr(settings, 'FACEBOOK_CLIENT_SECRET', None)
settings.FACEBOOK_VALIDATION_URL = getattr(settings, 'FACEBOOK_VALIDATION_URL', 'https://graph.facebook.com/debug_token?input_token=%s&access_token=%s|%s')