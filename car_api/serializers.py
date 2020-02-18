from rest_framework import serializers
from car_api.models import Customer, Car, Reservation

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','name','email','phone']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','vehicle_number','model','seating_capacity','rent_per_day']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id','customer','car','issue_date','return_date']

class CarReservationSerializer(serializers.Serializer):
    car = CarSerializer()
    reservations = ReservationSerializer(many=True)