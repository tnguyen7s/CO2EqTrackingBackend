from django.contrib import admin

from record.models import Electricity, Flight, Fuel, Meal, Transport

# Register your models here.
admin.site.register(Electricity)
admin.site.register(Fuel)
admin.site.register(Flight)
admin.site.register(Meal)
admin.site.register(Transport)