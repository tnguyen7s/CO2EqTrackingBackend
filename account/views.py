
from email.policy import HTTP
import pytz
import datetime

from django.conf import settings

from account.models import Consumer
from account.serializers import UserSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

#################################################### END-OF-IMPORT #################################################

def generate_auth_response_with_token(user):
    token, created = Token.objects.get_or_create(user=user)

    # regenarate token if it is expired
    utc_now = datetime.datetime.utcnow() 
    utc_now = utc_now.replace(tzinfo=pytz.utc)
   
    if not created and token.created < utc_now - settings.TIMED_AUTH_TOKEN['DEFAULT_VALIDITY_DURATION']:
        token.delete()
        token = Token.objects.create(user=user)
        token.created = datetime.datetime.utcnow()
        token.save()

    return Response({
        'id': user.pk,
        'username': user.username,
        'email': user.email,
        'refresh_token': token.key,
        'token_expiration_date': token.created + settings.TIMED_AUTH_TOKEN['DEFAULT_VALIDITY_DURATION']
    })


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        
        if (serializer.is_valid()):
            # create auth user
            serializer.save()

            # create a consumer record in the consumer table that references the auth.user
            consumer = Consumer.objects.create(user=serializer.instance, id=serializer.instance.id)
            consumer.save()
            
            return generate_auth_response_with_token(serializer.instance)
        else:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        if (serializer.is_valid()):
            user = serializer.validated_data['user']

            return generate_auth_response_with_token(user)
        else:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
        