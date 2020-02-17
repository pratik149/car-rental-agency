from django.contrib import admin
from car_api.models import Customer, Car, Reservation

# Register your models here.
admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Reservation)
