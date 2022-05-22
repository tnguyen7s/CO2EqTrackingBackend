import datetime
from django.utils.timezone import utc
import pytz
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings

# Override the TokenAuthentication, also set ExpiringTokenAuthenticationin settings.py
class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        if token.created + settings.TIMED_AUTH_TOKEN['DEFAULT_VALIDITY_DURATION'] < utc_now:
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)