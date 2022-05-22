#import those from django
from django.http import Http404

#import those from rest_framework
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

#import models
from record.models import *
#import serializers
from record.serializers import *


#################################################### END-OF-IMPORT #################################################

# Create your views here.
# https://www.django-rest-framework.org/api-guide/viewsets/
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
class FlightViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def list(self, request, date=None):
        result = self.queryset.filter(date=date)
        
        if (len(result)==0):
            raise Http404

        serializer = FlightSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_many(self, request, date=None):
        serializer = FlightSerializer(data=request.data, many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy_many(self, request, date=None):
        result = self.queryset.filter(date=date)
        result.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ElectricityViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ElectricitySerializer
    queryset = Electricity.objects.all()

    def create(self, request, date=None):
        serializer = ElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, date=None):
        result = self.queryset.filter(date=date)

        if (len(result)==0):
            raise Http404

        serializer = ElectricitySerializer(instance=result[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, date=None):
        pass


    def destroy(self, request, date=None):
        result = self.queryset.filter(date=date)
        result.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class FuelViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FuelSerializer
    queryset = Fuel.objects.all()

    def list(self, request, date=None):
        result = self.queryset.filter(date=date)

        if (len(result)==0):
            raise Http404

        serializer = FuelSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create_many(self, request, date=None):
        serializer = FuelSerializer(data=request.data, many=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)

    def destroy_many(self, request, date=None):
        result = self.queryset.filter(date=date)
        result.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class MealViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MealSerializer
    queryset = Meal.objects.all()

    def list(self, request, date=None):
        result = self.queryset.filter(date=date)

        if (len(result)==0):
            raise Http404

        serializer = MealSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create_many(self, request, date=None):
        serializer = MealSerializer(data=request.data, many=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)

    def destroy_many(self, request, date=None):
        result = self.queryset.filter(date=date)
        result.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class TransportViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()

    def create(self, request, date=None):
        serializer = TransportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, date=None):
        result = self.queryset.filter(date=date)

        if (len(result)==0):
            raise Http404

        serializer = TransportSerializer(instance=result[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, date=None):
        pass

    def destroy(self, request, date=None):
        result = self.queryset.filter(date=date)
        result.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)