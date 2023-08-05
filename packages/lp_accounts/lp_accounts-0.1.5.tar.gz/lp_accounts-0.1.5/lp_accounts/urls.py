from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AccountCreate, AccountDetails, PasswordReset, PasswordUpdate, ObtainAuthToken

urlpatterns = {
    url(r'^account/create$', AccountCreate.as_view(), name='lp_accounts_create'),
    url(r'^account$', AccountDetails.as_view(), name='lp_accounts_retrieve'),
    url(r'^account/password/reset', PasswordReset.as_view(), name='password_reset'),
    url(r'^account/password/update', PasswordUpdate.as_view(), name='password_update'),
    url(r'^login/', ObtainAuthToken.as_view(), name='login')
}

urlpatterns = format_suffix_patterns(urlpatterns)
