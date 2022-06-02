import json
from turtle import distance
from rest_framework.test import APITestCase

from account.models import Consumer
from record.models import Electricity, Flight, Fuel, Meal, Transport
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from record.serializers import ElectricitySerializer, FlightSerializer, FuelSerializer, MealSerializer, TransportSerializer

# Django uses a separate database from whatever database we access in out development and destroys it after running all tests.
# Create your tests here.
class FlightViewSetTestCase(APITestCase):
    # Django automatically know to run this method before running any methods starting with test_
    def setUp(self):
        # create a dummy consumer in the database
        self.email="tnguyen7s@semo.edu"
        self.username="tnguyen7s"
        self.password="hanh312$"

        self.user = User.objects.create(email = self.email, username = self.username, password = self.password)
        self.consumer = Consumer.objects.create(user=self.user, id=self.user.id)
        self.token = Token.objects.create(user=self.user)

        # create a second dummy consumer 
        self.email2="tnguyen7s2@semo.edu"
        self.username2="tnguyen7s2"
        self.password2="hanh312$2"

        self.user2 = User.objects.create(email = self.email2, username = self.username2, password = self.password2)
        self.consumer2 = Consumer.objects.create(user=self.user2, id=self.user2.id)
        self.token2 = Token.objects.create(user=self.user2)

        # date is used
        self.date = '2022-05-27'

        # a list of flights that is sent to the api
        self.flights = [
            {
                'date': self.date, 
                'source_iata': 'STL', 
                'destination_iata': 'HNA', 
                'cabin_class': 'BUSINESS', 
                'source_name': 'Saint Louis International Airport', 
                'destination_name': 'Haneda Airport', 
                'kg_co2eq': 1000, 
                'consumer': self.consumer.id
            },
            {
                'date': self.date, 
                'source_iata': 'HNA', 
                'destination_iata': 'SGN', 
                'cabin_class': 'BUSINESS', 
                'source_name': 'Haneda Aiport', 
                'destination_name': 'Tan Son Nhat International Aiport', 
                'kg_co2eq': 500, 
                'consumer': self.consumer.id
            }
        ]
         
        # URL 
        self.url = '/record/flights/'+self.date     

    def create_dummy_two_flight_entities(self, consumer):
         # save dummy flights of the given date to dummy database
        first_saved_flight = Flight.objects.create(date=self.date, 
                                                        source_iata='STL', 
                                                        destination_iata='HNA', 
                                                        cabin_class="BUSINESS",
                                                        source_name='Saint Louis International Airport',
                                                        destination_name='Haneda Airport',
                                                        kg_co2eq=1000,
                                                        consumer=consumer)
        second_saved_flight =  Flight.objects.create(date=self.date, 
                                                        source_iata='HNA', 
                                                        destination_iata='SGN', 
                                                        cabin_class="BUSINESS",
                                                        source_name='Haneda Airport',
                                                        destination_name='Tan SoN Nhat Airport',
                                                        kg_co2eq=500,
                                                        consumer=consumer)   
        return first_saved_flight, second_saved_flight

    def test_list_return_list_of_flights_when_path_happy(self):
        # Arrange
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # with force_authenticate, no need to send a token
        self.client.force_authenticate(user=self.user)
        first_saved_flight, second_saved_flight = self.create_dummy_two_flight_entities(self.consumer)

        # Act
        response = self.client.get(self.url)
        data = json.loads(response.content)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], FlightSerializer(instance=first_saved_flight).data)
        self.assertEqual(data[1], FlightSerializer(instance=second_saved_flight).data)


    def test_create_many_save_flights_to_db_when_path_happy(self):
        # Arrange
        Flight.objects.all().delete()
        self.client.force_authenticate(user=self.user)

        # ACt
        response = self.client.post(self.url, self.flights)
        db_flights = Flight.objects.filter(date=self.date)
        print(response.data)

        # Assert
        self.assertEqual(201, response.status_code) 
        self.assertEqual(len(db_flights), 2)
        self.assertEqual(db_flights[0].kg_co2eq, self.flights[0]['kg_co2eq'])
        self.assertEqual(db_flights[1].kg_co2eq, self.flights[1]['kg_co2eq'])

    def test_destroy_many_delete_flights_from_db_when_path_happy(self):
        # Arrange
        Flight.objects.all().delete()
        self.create_dummy_two_flight_entities(self.consumer)
        self.create_dummy_two_flight_entities(self.consumer2)
        self.client.force_authenticate(user=self.user2) # send request under the authentication from the second consumer

        # Act 
        response =self.client.delete(self.url)
        flights_left_in_db = Flight.objects.all()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertEqual(len(flights_left_in_db), 2)
        self.assertEqual(flights_left_in_db[0].consumer.id, self.consumer.id)
        
    
class ElectricityViewSetTestCase(APITestCase):
    def setUp(self):
        # create a dummy consumer in the database
        self.email="tnguyen7s@semo.edu"
        self.username="tnguyen7s"
        self.password="hanh312$"

        self.user = User.objects.create(email = self.email, username = self.username, password = self.password)
        self.consumer = Consumer.objects.create(user=self.user, id=self.user.id)

        # create a second dummy consumer 
        self.email2="tnguyen7s2@semo.edu"
        self.username2="tnguyen7s2"
        self.password2="hanh312$2"

        self.user2 = User.objects.create(email = self.email2, username = self.username2, password = self.password2)
        self.consumer2 = Consumer.objects.create(user=self.user2, id=self.user2.id)

        # date is used
        self.date = '2022-05-27'

        # electricity instance that is used to be sent to the api
        self.electricity= {
            "date": self.date, 
            "value": 23, 
            "units": "Wh", 
            "kg_co2eq": 0.02, 
            "consumer": self.consumer.id
        }
         
        # URL 
        self.url = '/record/electricity/'+self.date     

    def create_dummy_electricity_entity(self, consumer):
         # save dummy electricity of the given date to our dummy database
        saved_electricity = Electricity.objects.create( date=self.date, 
                                                        value = 23,
                                                        units = "Wh", 
                                                        kg_co2eq = 0.02,
                                                        consumer = consumer)

        return saved_electricity

    def test_retrieve_return_electricity_data_when_path_happy(self):
        # Arrange
        # with force_authenticate, no need to send a token
        self.client.force_authenticate(user=self.user)
        saved_electricity = self.create_dummy_electricity_entity(self.consumer)
        self.create_dummy_electricity_entity(self.consumer2)

        # Act
        response = self.client.get(self.url)
        data = json.loads(response.content)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(data, ElectricitySerializer(instance=saved_electricity).data)


    def test_create_save_electricity_to_db_when_path_happy(self):
        # Arrange
        Electricity.objects.all().delete()
        self.client.force_authenticate(user=self.user)

        # ACt
        response = self.client.post(self.url, self.electricity)
        db_electricity= Electricity.objects.filter(date=self.date).filter(consumer = self.consumer)

        # Assert
        self.assertEqual(201, response.status_code) 
        self.assertEqual(len(db_electricity), 1)
        self.assertEqual(db_electricity[0].kg_co2eq, self.electricity['kg_co2eq'])

    def test_destroy_delete_electricity_from_db_when_path_happy(self):
        # Arrange
        Flight.objects.all().delete()
        self.create_dummy_electricity_entity(self.consumer)
        self.create_dummy_electricity_entity(self.consumer2)
        self.client.force_authenticate(user=self.user2) # send request under the authentication from the second consumer

        # Act 
        response =self.client.delete(self.url)
        electricity_left_in_db = Electricity.objects.all()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertEqual(len(electricity_left_in_db), 1)
        self.assertEqual(electricity_left_in_db[0].consumer.id, self.consumer.id)

class FuelViewSetTestCase(APITestCase):
    def setUp(self):
        # create a dummy consumer in the database
        self.email="tnguyen7s@semo.edu"
        self.username="tnguyen7s"
        self.password="hanh312$"

        self.user = User.objects.create(email = self.email, username = self.username, password = self.password)
        self.consumer = Consumer.objects.create(user=self.user, id=self.user.id)

        # create a second dummy consumer 
        self.email2="tnguyen7s2@semo.edu"
        self.username2="tnguyen7s2"
        self.password2="hanh312$2"

        self.user2 = User.objects.create(email = self.email2, username = self.username2, password = self.password2)
        self.consumer2 = Consumer.objects.create(user=self.user2, id=self.user2.id)

        # date is used
        self.date = '2022-05-27'

        # fuel instances that are used to be sent to the api
        self.fuels= [
            {
                "date": self.date,
                "type": "petrol",
                "value": 10,
                "units": "liters",
                "kg_co2eq": 75.37,
                "consumer": self.consumer.id
            },
            {
                "date": self.date,
                "type": "natural_gas",
                "value": 10,
                "units": "gallons",
                "kg_co2eq": 75.37,
                "consumer": self.consumer.id
            }
        ]
         
        # URL 
        self.url = '/record/fuels/'+self.date     

    def create_two_dummy_fuel_entities(self, consumer):
         # save dummy electricity of the given date to our dummy database
        first_saved_fuel = Fuel.objects.create(date=self.date,
                                                type = 'petrol',
                                                value = 10,
                                                units = "liters", 
                                                kg_co2eq = 75.37,
                                                consumer = consumer)

        second_saved_fuel = Fuel.objects.create(date=self.date,
                                                type = 'natural_gas',
                                                value = 10,
                                                units = "gallons", 
                                                kg_co2eq = 75.37,
                                                consumer = consumer)

        return first_saved_fuel, second_saved_fuel

    def test_list_return_fuels_data_when_path_happy(self):
        # Arrange
        # with force_authenticate, no need to send a token
        self.client.force_authenticate(user=self.user)
        first_saved_fuel, second_saved_fuel = self.create_two_dummy_fuel_entities(self.consumer)
        self.create_two_dummy_fuel_entities(self.consumer2)

        # Act
        response = self.client.get(self.url)
        data = json.loads(response.content)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(data))
        self.assertEqual(data[0], FuelSerializer(instance=first_saved_fuel).data)


    def test_create_many_save_fuels_to_db_when_path_happy(self):
        # Arrange
        Fuel.objects.all().delete()
        self.client.force_authenticate(user=self.user)

        # ACt
        response = self.client.post(self.url, self.fuels)
        db_fuels= Fuel.objects.filter(date=self.date).filter(consumer = self.consumer)
        print(response.data)

        # Assert
        self.assertEqual(201, response.status_code) 
        self.assertEqual(len(db_fuels), 2)
        self.assertEqual(db_fuels[0].kg_co2eq, self.fuels[0]['kg_co2eq'])

    def test_destroy_delete_fuels_from_db_when_path_happy(self):
        # Arrange
        Fuel.objects.all().delete()
        self.create_two_dummy_fuel_entities(self.consumer)
        self.create_two_dummy_fuel_entities(self.consumer2)
        self.client.force_authenticate(user=self.user2) # send request under the authentication from the second consumer

        # Act 
        response =self.client.delete(self.url)
        fuels_left_in_db = Fuel.objects.all()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertEqual(len(fuels_left_in_db), 2)
        self.assertEqual(fuels_left_in_db[0].consumer.id, self.consumer.id)

class MealViewSetTestCase(APITestCase):
    def setUp(self):
        # create a dummy consumer in the database
        self.email="tnguyen7s@semo.edu"
        self.username="tnguyen7s"
        self.password="hanh312$"

        self.user = User.objects.create(email = self.email, username = self.username, password = self.password)
        self.consumer = Consumer.objects.create(user=self.user, id=self.user.id)

        # create a second dummy consumer 
        self.email2="tnguyen7s2@semo.edu"
        self.username2="tnguyen7s2"
        self.password2="hanh312$2"

        self.user2 = User.objects.create(email = self.email2, username = self.username2, password = self.password2)
        self.consumer2 = Consumer.objects.create(user=self.user2, id=self.user2.id)

        # date is used
        self.date = '2022-05-27'

        # meal instances that are used to be sent to the api
        self.meals= [
             {
                "date": self.date,
                "meal": "breakfast",
                "food_products": "['Milk (cow)']",
                "kg_co2eq": 0.628,
                "consumer": self.consumer.id
             },
             {
                "date": self.date,
                "meal": "lunch",
                "food_products": "['Rice','Tomatoes','Apple','Pork']",
                "kg_co2eq": 2.327,
                "consumer": self.consumer.id
            },
            {
                "date": self.date,
                "meal": "dinner",
                "food_products": "['Pasta','Beef']",
                "kg_co2eq": 7.88,
                "consumer": self.consumer.id
            }
        ]
         
        # URL 
        self.url = '/record/meals/'+self.date     

    def create_dummy_meal_entity(self, consumer):
         # save dummy meal of the given date to our dummy database
        saved_meal = Meal.objects.create(date=self.date,
                                        meal = "dinner",
                                        food_products = "['Pasta','Beef']",
                                        kg_co2eq = 7.88,
                                        consumer = consumer)


        return saved_meal

    def test_list_return_meals_data_when_path_happy(self):
        # Arrange
        # with force_authenticate, no need to send a token
        self.client.force_authenticate(user=self.user)
        first_saved_meal = self.create_dummy_meal_entity(self.consumer)
        self.create_dummy_meal_entity(self.consumer2)

        # Act
        response = self.client.get(self.url)
        data = json.loads(response.content)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(data))
        self.assertEqual(data[0], MealSerializer(instance=first_saved_meal).data)


    def test_create_many_save_meals_to_db_when_path_happy(self):
        # Arrange
        Meal.objects.all().delete()
        self.client.force_authenticate(user=self.user)

        # ACt
        response = self.client.post(self.url, self.meals)
        db_meals= Meal.objects.filter(date=self.date).filter(consumer = self.consumer)

        # Assert
        self.assertEqual(201, response.status_code) 
        self.assertEqual(len(db_meals), 3)
        self.assertEqual(db_meals[0].kg_co2eq, self.meals[0]['kg_co2eq'])

    def test_destroy_delete_meals_from_db_when_path_happy(self):
        # Arrange
        Meal.objects.all().delete()
        self.create_dummy_meal_entity(self.consumer)
        self.create_dummy_meal_entity(self.consumer2)
        self.client.force_authenticate(user=self.user2) # send request under the authentication from the second consumer

        # Act 
        response =self.client.delete(self.url)
        meals_left_in_db = Meal.objects.all()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertEqual(len(meals_left_in_db), 1)
        self.assertEqual(meals_left_in_db[0].consumer.id, self.consumer.id)

class TransportViewSetTestCase(APITestCase):
    def setUp(self):
        # create a dummy consumer in the database
        self.email="tnguyen7s@semo.edu"
        self.username="tnguyen7s"
        self.password="hanh312$"

        self.user = User.objects.create(email = self.email, username = self.username, password = self.password)
        self.consumer = Consumer.objects.create(user=self.user, id=self.user.id)

        # create a second dummy consumer 
        self.email2="tnguyen7s2@semo.edu"
        self.username2="tnguyen7s2"
        self.password2="hanh312$2"

        self.user2 = User.objects.create(email = self.email2, username = self.username2, password = self.password2)
        self.consumer2 = Consumer.objects.create(user=self.user2, id=self.user2.id)

        # date is used
        self.date = '2022-05-27'

        # transport instance that is used to be sent to the api
        self.transport= {
            "date": self.date, 
            "distance": 40, 
            "distance_unit": "km", 
            "fuel_efficiency": 22, 
            "fuel_eff_unit": "mpg", 
            "fuel_type": "gasoline", 
            "kg_co2eq": 10.01, 
            "consumer": self.consumer.id
        }
         
        # URL 
        self.url = '/record/transport/'+self.date     

    def create_dummy_transport_entity(self, consumer):
         # save dummy transport of the given date to our dummy database
        saved_transport = Transport.objects.create( date=self.date, 
                                                    distance = 40,
                                                    distance_unit = "km",
                                                    fuel_efficiency = 22,
                                                    fuel_eff_unit = "mpg",
                                                    fuel_type = "gasoline",
                                                    kg_co2eq = 10.01,
                                                    consumer = consumer)

        return saved_transport

    def test_retrieve_return_transport_data_when_path_happy(self):
        # Arrange
        # with force_authenticate, no need to send a token
        self.client.force_authenticate(user=self.user)
        saved_transport = self.create_dummy_transport_entity(self.consumer)
        self.create_dummy_transport_entity(self.consumer2)

        # Act
        response = self.client.get(self.url)
        data = json.loads(response.content)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(data, TransportSerializer(instance=saved_transport).data)


    def test_create_save_transport_to_db_when_path_happy(self):
        # Arrange
        Transport.objects.all().delete()
        self.client.force_authenticate(user=self.user)

        # ACt
        response = self.client.post(self.url, self.transport)
        db_transport= Transport.objects.filter(date=self.date).filter(consumer = self.consumer)

        # Assert
        self.assertEqual(201, response.status_code) 
        self.assertEqual(len(db_transport), 1)
        self.assertEqual(db_transport[0].kg_co2eq, self.transport['kg_co2eq'])

    def test_destroy_delete_transport_from_db_when_path_happy(self):
        # Arrange
        Transport.objects.all().delete()
        self.create_dummy_transport_entity(self.consumer)
        self.create_dummy_transport_entity(self.consumer2)
        self.client.force_authenticate(user=self.user2) # send request under the authentication from the second consumer

        # Act 
        response =self.client.delete(self.url)
        transport_left_in_db = Transport.objects.all()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertEqual(len(transport_left_in_db), 1)
        self.assertEqual(transport_left_in_db[0].consumer.id, self.consumer.id)