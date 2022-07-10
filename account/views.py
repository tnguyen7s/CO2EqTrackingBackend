from django.conf import settings
import pytz
import datetime
from account.models import Consumer
from account.serializers import UserSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
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
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        print('here1')

        try:
            if (serializer.is_valid()):
                # create auth user
                serializer.save()
                print('here2')


                # create a consumer record in the consumer table that references the auth.user
                consumer = Consumer.objects.create(user=serializer.instance, id=serializer.instance.id)
                consumer.save()

                print('here3')
                return generate_auth_response_with_token(serializer.instance)
            else:
                return Response(serializer.errors, status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print("Exception", e)

class AccountViewSetUpdate(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated] 
    # update
    def update(self, request):
        try:
            # get the consumer object
            consumer = Consumer.objects.get(pk=request.user.id)

            # get the user objecy
            user = User.objects.get(pk=request.user.id)

            # serialize the request data
            user.email=request.data['email'] if 'email' in request.data and not request.data['email']=='' else user.email
            user.username=request.data['username'] if 'username'in request.data and not request.data['username']=='' else user.username
            user.first_name = request.data['first_name'] if  'first_name' in request.data else user.first_name
            user.last_name = request.data['last_name'] if 'last_name' in request.data else user.last_name
            consumer.birthdate = request.data['birthdate'] if 'birthdate' in request.data else consumer.birthdate
            consumer.gender = request.data['gender'] if 'gender' in request.data else consumer.gender
            consumer.country = request.data['country'] if 'country' in request.data else consumer.country
            consumer.city = request.data['city'] if 'city' in request.data else consumer.city
            consumer.region = request.data['region'] if 'region' in request.data else consumer.region

        
            user.save()
            consumer.save()
        except Exception as e:
            print('Error', e)
            return Response(e, status.HTTP_400_BAD_REQUEST)

        return Response('Data is updated.', status.HTTP_200_OK)

    def retrieve(self, request):
        consumer = Consumer.objects.get(pk=request.user.id)
        user = User.objects.get(pk=request.user.id)

        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birthdate': consumer.birthdate,
            'gender': consumer.gender,
            'country': consumer.country,
            'city': consumer.city,
            'region': consumer.region
        }

        return Response(data, status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if (serializer.is_valid()):
            try:
                user = serializer.validated_data['user']
                return generate_auth_response_with_token(user)
            except Exception as e:
                print(e)
        else:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
        