from record.models import Electricity, Flight, Fuel, Meal, Transport
from rest_framework import serializers

#################################################### END-OF-IMPORT #################################################


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'date', 'source_iata', 'destination_iata', 'cabin_class', 'source_name', 'destination_name', 'kg_co2eq', 'user']

class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Electricity
        fields = ['id', 'date', 'value', 'units', 'kg_co2eq', 'user']

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = ['id', 'date', 'type', 'value', 'units', 'kg_co2eq', 'user'] 

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'date', 'meal', 'food_products', 'kg_co2eq', 'user']

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['id', 'date', 'distance', 'distance_unit', 'fuel_efficiency', 'fuel_eff_unit', 'fuel_type', 'kg_co2eq', 'user']