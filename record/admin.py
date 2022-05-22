from django.contrib import admin

from record.models import Electricity, Flight, Fuel, Meal, Transport, User

# Register your models here.
admin.site.register(Electricity)
admin.site.register(Fuel)
admin.site.register(Flight)
admin.site.register(Meal)
admin.site.register(Transport)
admin.site.register(User)