from record.models import Electricity, Flight, Fuel, Meal, Transport
from rest_framework import serializers

#################################################### END-OF-IMPORT #################################################

class RecordCreation:
    def create_flight(data):
        date = data['date']
        month = date.month
        flight = Flight(date=data['date'], 
                        month = month,
                        source_iata=data['source_iata'], 
                        destination_iata=data['destination_iata'], 
                        cabin_class=data['cabin_class'],
                        source_name = data['source_name'],
                        destination_name = data['destination_name'],
                        kg_co2eq = data['kg_co2eq'],
                        consumer = data['consumer']
                        )
        flight.save()
        return flight

    def create_electricity(data):
        date = data['date']
        month = date.month
        electricity = Electricity(date=data['date'], 
                        month = month,
                        value=data['value'], 
                        units=data['units'], 
                        kg_co2eq = data['kg_co2eq'],
                        consumer = data['consumer']
                        )
        electricity.save()

        return electricity

    def create_fuel(data):
        date = data['date']
        month = date.month
        fuel = Fuel(date=data['date'], 
                    month = month,
                    type = data['type'],
                    value=data['value'], 
                    units=data['units'], 
                    kg_co2eq = data['kg_co2eq'],
                    consumer = data['consumer']
                    )
        fuel.save()
        return fuel

    def create_meal(data):
        date = data['date']
        month = date.month
        meal = Meal(date=data['date'], 
                    month = month,
                    meal = data['meal'],
                    food_products=data['food_products'], 
                    kg_co2eq = data['kg_co2eq'],
                    consumer = data['consumer']
                    )
        meal.save()
        return meal

    def create_transport(data):
        date = data['date']
        month = date.month
        transport = Transport(date=data['date'], 
                    month = month,
                    distance = data['distance'],
                    distance_unit = data['distance_unit'],
                    fuel_efficiency = data['fuel_efficiency'],
                    fuel_eff_unit = data['fuel_eff_unit'],
                    fuel_type = data['fuel_type'],
                    kg_co2eq = data['kg_co2eq'],
                    consumer = data['consumer']
        )
        transport.save()
        return transport

'''
Flight Serializers
'''
class FlightListSerializer(serializers.ListSerializer):
    def create(self, data_list):
        flight_list = []

        for data in data_list:
            newly_created_flight = RecordCreation.create_flight(data)
        
            flight_list.append(newly_created_flight)

        return flight_list

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FlightListSerializer
        model = Flight
        fields = ['id', 'date', 'source_iata', 'destination_iata', 'cabin_class', 'source_name', 'destination_name', 'kg_co2eq', 'consumer']   

    def create(self, data):
        return RecordCreation.create_flight(data)


'''
Electricity Serializers
'''
class ElectricityListSerializer(serializers.ListSerializer):
    def create(self, data_list):
        electricity_list = []

        for data in data_list:
            electricity = RecordCreation.create_electricity(data)
            electricity_list.append(electricity)

        return electricity_list

class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = ElectricityListSerializer
        model = Electricity
        fields = ['id', 'date', 'value', 'units', 'kg_co2eq', 'consumer']

    def create(self, data):
       return RecordCreation.create_electricity(data)

'''
Fuel Serializers
'''
class FuelListSerializer(serializers.ListSerializer):
    def create(self, data_list):
        fuel_list = []

        for data in data_list:
            fuel = RecordCreation.create_fuel(data)
            fuel_list.append(fuel)

        return fuel_list

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FuelListSerializer
        model = Fuel
        fields = ['id', 'date', 'type', 'value', 'units', 'kg_co2eq', 'consumer'] 

    def create(self, data):
        return RecordCreation.create_fuel(data)
       
'''
Meal Serializers
'''
class MealListSerializer(serializers.ListSerializer):
    def create(self, data_list):
        meal_list = []

        for data in data_list:
            meal = RecordCreation.create_meal(data)
            meal_list.append(meal)

        return meal_list
        

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = MealListSerializer
        model = Meal
        fields = ['id', 'date', 'meal', 'food_products', 'kg_co2eq', 'consumer']

    def create(self, data):
        return RecordCreation.create_meal(data)
    
'''
Transport serializers
'''
class TransportListSerializer(serializers.ListSerializer):
    def create(self, data_list):
        transport_list = []

        for data in data_list:
            meal = RecordCreation.create_transport(data)
            transport_list.append(meal)

        return transport_list

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = TransportListSerializer
        model = Transport
        fields = ['id', 'date', 'distance', 'distance_unit', 'fuel_efficiency', 'fuel_eff_unit', 'fuel_type', 'kg_co2eq', 'consumer']

    def create(self, data):
        return RecordCreation.create_transport(data)
