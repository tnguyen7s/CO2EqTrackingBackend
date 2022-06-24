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
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )

        user.set_password(validated_data['password'])

        user.save()
        return 
        
# class ConsumerPhotoSerializer(serializers.ModelSerializer):
#     photo = serializers.ImageField(
#         max_length=None,
#         use_url=True
#     )

#     class Meta:
#         model = Consumer
#         fields = ["photo"]

        