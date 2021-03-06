from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
CONSUMER MODEL
"""
def user_directory_path(instance, filename):
    return f'user_{instance.consumer.id}/{filename}'
class Consumer(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False, auto_created=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)
    country = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)

   
