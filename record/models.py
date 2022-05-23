from django.db import models
from account.models import Consumer

# Create your models here.
"""
FLIGHT MODEL
date: string;
sourceIATA: string;
destinationIATA: string;
cabinClass: string;  [ECONOMY, BUSINESS, FIRST]
sourceName?: string;
destinationName?:string;
co2eInKg: number; 
"""
class Flight(models.Model):
    CABIN_CHOICES = (
        ('ECONOMY', 'Economy'),
        ('BUSINESS', 'Business'),
        ('FIRST', 'First')
    )
    date = models.DateField(null=False)
    source_iata = models.CharField(max_length=3, null=False)
    destination_iata = models.CharField(max_length=3, null=False)
    cabin_class = models.CharField(max_length=10, null=False, choices=CABIN_CHOICES)
    source_name = models.CharField(max_length=100)
    destination_name = models.CharField(max_length=100)
    kg_co2eq = models.FloatField(null=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, default=-1)

    def __str__(self):
        return self.date + "\n" + self.source_name + "\n" + self.destination_name + "\n" + self.kg_co2eq + "kgCO2eq"

"""
ELECTRICITY MODEL
date: string;
value: number; [WH,KWH,MWH]
units: string;
co2eInKg: number;
"""
class Electricity(models.Model):
    E_UNIT_CHOICES = (
        ('Wh', 'Wh'),
        ('kWh', 'kWh'),
        ('mWh', 'mWh')
    )
    date = models.DateField(null=False)
    value = models.FloatField(null=False)
    units = models.CharField(max_length=10, null=False, choices=E_UNIT_CHOICES)
    kg_co2eq = models.FloatField(null=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, default=-1)

    def __str__(self):
        return self.date + "\n" + self.value + "\n" + self.units + "\n" + self.kg_co2eq + "kgCO2eq"



"""
FUEL MODEL
date: string;
type: string; [diesel, gasoline, petrol, butane, natural_gas, propane]
value: number;
units: string;
co2eInKg?: number;
"""
class Fuel(models.Model):
    F_UNIT_CHOICES = (
        ("tonnes", "tonnes"),
        ("liters", "liters"),
        ("gallons", "gallons"),
        ("uk_therms", "uk_therms"),
        ("us_therms", "us_therms"),
        ("MMBtu", "MMBtu"),
        ("cubic_meters", "cubic_meters")
    )

    F_CHOICES = (
        ('diesel', 'diesel'),
        ('gasoline', 'gasoline'),
        ('petrol', 'petrol'),
        ('butane', 'butane'),
        ('natural_gas', 'natural_gas'),
        ('propane', 'propane'),
        ('kerosene', 'kerosene'),
        ('fuel_oil', 'fuel_oil'),
        ('gas_oil', 'gas_oil')
    )

    date = models.DateField(null=False)
    type = models.CharField(max_length=15, null=False, choices=F_CHOICES)
    value = models.FloatField(null=False)
    units = models.CharField(max_length=15, null=False, choices=F_UNIT_CHOICES)
    kg_co2eq = models.FloatField(null=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, default=-1)

    def __str__(self):
        return self.date + "\n" + self.type + "\n" + self.value + "\n" + self.units + "\n" + self.kg_co2eq + "kgCO2eq"

"""
MEAL MODEL
date: string
meal: string
foodProducts: string[]
totalEco2InKg: number
"""
class Meal(models.Model):
    MEAL_CHOICES = (
        ("breakfast", "breakfast"),
        ("lunch", "lunch"),
        ("dinner", "dinner")
    )
    date = models.DateField(null=False)
    meal = models.CharField(max_length=10, null=False, choices=MEAL_CHOICES)
    food_products = models.CharField(max_length=255, null=False)
    kg_co2eq = models.FloatField(null=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, default=-1)

    def __str__(self):
        return self.date + "\n" + self.meal + "\n" + self.food_products + "\n" + self.kg_co2eq + "kgCO2eq"


"""
TRANSPORT MODEL
date: string,
distance: number,
distUnit: string,
fuelEfficiency: number,
fuelEfUnit: string,
fuelType: string,
eCo2InKg: number
"""
class Transport(models.Model):
    DISTANCE_UNIT_CHOICES = (
        ("km", "km"),
        ("miles", "miles")
    )

    FUEL_EFF_UNIT_CHOICES = (
        ("mpg", "mpg"),
        ("km/l", "km/l"),
        ("1/100km", "1/100km")
    )

    FUEL_TYPE = (
        ("gasoline", "gasoline"),
        ("diesel", "diesel")
    )

    date = models.DateField(null=False)
    distance =  models.PositiveSmallIntegerField(null=False)
    distance_unit = models.CharField(max_length=10, null=False, choices=DISTANCE_UNIT_CHOICES)
    fuel_efficiency = models.PositiveSmallIntegerField(null=False)
    fuel_eff_unit = models.CharField(max_length=10, null=False, choices=FUEL_EFF_UNIT_CHOICES)
    fuel_type = models.CharField(max_length=10, null=False, choices=FUEL_TYPE)
    kg_co2eq = models.FloatField(null=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, default=-1)

    def __str__(self):
        return self.date + "\n" + self.distance + self.distance_unit + "\n" + self.fuel_efficiency + self.fuel_eff_unit + "\n" + self.fuel_type + "\n" + self.kg_co2eq + "kgCO2eq"

