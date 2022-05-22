# import basic URL configuration
from django.urls import include, path

# import format_suffix_patterns
from rest_framework.urlpatterns import format_suffix_patterns

# import all views
from .views import *

#################################################### END-OF-IMPORT #################################################

# bind ViewSet classes into a set of concrete views
flight_list = FlightViewSet.as_view({
    'get': 'list',
    'post': 'create_many',
    'delete': 'destroy_many',
})

electricity_detail = ElectricityViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})

fuel_list = FuelViewSet.as_view({
    'get': 'list',
    'post': 'create_many',
    'delete': 'destroy_many',
})

meal_list = MealViewSet.as_view({
    'get': 'list',
    'post': 'create_many',
    'delete': 'destroy_many'
})

transport_detail = TransportViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})

# register the views with the URL
urlpatterns = format_suffix_patterns([
    path('flights/<str:date>', flight_list),
    path('electricity/<str:date>', electricity_detail),
    path('fuels/<str:date>', fuel_list),
    path('meals/<str:date>', meal_list),
    path('transport/<str:date>', transport_detail)
])

