from collections import namedtuple
from datetime import datetime, date

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from car_api.models import Car, Reservation
from car_api.serializers import (CarSerializer, ReservationSerializer, CarReservationSerializer)


@api_view(['GET'])
def home(request):
    """
    API endpoint for home page.
    """
    if request.method == 'GET':
        data = [{'message':'Welcome to Car-Rental-Agency'}]
        return JsonResponse(data, safe=False)


@api_view(['GET'])
def view_all_cars(request):
    """
    API endpoint for displaying all car details.
    """
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_car_details(request, pk):
    """
    API endpoint for displaying particular car details.
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)


@api_view(['GET'])
def view_car_details_active_booking(request, pk):
    """
    API endpoint for displaying specific car details with
    its current active reservation details.
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        current_date = date.today()
        CarBookingDetails = namedtuple('CarBookingDetails',('car','current_active_bookings'))

        # Conditions for filtering only currently active bookings of a particular car
        # suffix "__gte" stands for Greater Than or Equal to.
        condition_1 = Q(issue_date__gte=current_date)
        condition_2 = Q(return_date__gte=current_date)

        carBookingDetails = CarBookingDetails(
            car = car,
            current_active_bookings = Reservation.objects.filter(car=pk).filter(condition_1 | condition_2),
        )
        serializer = CarReservationSerializer(carBookingDetails)
        return Response(serializer.data)


@api_view(['POST'])
def add_car(request):
    """
    API endpoint for adding new car to the system,
    which could be used for renting.
    """
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_car_details(request, pk):
    """
    API endpoint for editing a particular car details.
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_car(request, pk):
    """
    API endpoint for deleting car from the system.
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@parser_classes([JSONParser])
def view_all_cars_on_given_date(request):
    """
    API endpoint for showing the cars with their availability status on a given date.
    And filter the cars based on various fields.
    """
    if request.method == 'POST':
        data = request.data
        
        check_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        print(type(check_date))
        print(check_date)

        # cars = Car.objects.all().filter(model=data['model'], seating_capacity=data['seating_capacity'])
        # serializer = CarSerializer(cars, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        # reservations = Reservation.objects.all().filter(car=car.id)

        cars = Car.objects.all()
        for car in cars:
            serializer = CarSerializer(car)
            reservations = Reservation.objects.all().filter(car=car.id)
            for r in reservations:
                if not r.issue_date <= check_date <= r.return_date:
                    # res = {"message":"No any cars are available on this date"}
                    # return Response(data=json.dumps(res), status=status.HTTP_200_OK)
                    return Response(serializer.data)
            return Response(serializer.data)
