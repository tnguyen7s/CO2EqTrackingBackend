import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from account.models import Consumer

#################################################### END-OF-IMPORT #################################################


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
            
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(min_length=8, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': { 'write_only': True }}

    #override the create method to apply hash to the password => security purposes
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])

        user.save()
        return user
        

        