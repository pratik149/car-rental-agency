from collections import namedtuple
from datetime import datetime, date

from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from car_api.models import Car, Reservation
from car_api.serializers import (CarSerializer, ReservationSerializer, CarDetailsReservationSerializer, AvailableCarSerializer)


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
def view_car_details(request, car_pk):
    """
    API endpoint for displaying particular car details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)


@api_view(['GET'])
def view_car_details_active_booking(request, car_pk):
    """
    API endpoint for displaying specific car details with
    its current active reservation details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
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
            current_active_bookings = Reservation.objects.filter(car=car_pk).filter(condition_1 | condition_2),
        )
        serializer = CarDetailsReservationSerializer(carBookingDetails)
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
def edit_car_details(request, car_pk):
    """
    API endpoint for editing a particular car details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_car(request, car_pk):
    """
    API endpoint for deleting car from the system.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@parser_classes([JSONParser])
def view_all_cars_on_given_date(request):
    """
    API endpoint for showing the cars with their availability status on a given date.
    And filter the cars based on various fields.
    """
    if request.method == 'GET':
        # Fetch date from url if passed or else set default to today's date.
        date_to_check = request.GET.get('date', str(date.today()) )
        date_to_check = datetime.strptime(date_to_check, '%Y-%m-%d').date() # Convert date to datetime format.
        
        # Fetch filters like model, capacity or availability status
        # if passed any as GET request URL parameters
        model = request.GET.get('model')
        capacity = request.GET.get('capacity')
        availability = request.GET.get('availability')

        # Filter all car reservations which falls in between date_to_check
        condition_1 = Q(issue_date__gte=date_to_check)
        condition_2 = Q(return_date__gte=date_to_check)
        reservations = Reservation.objects.filter(condition_1 | condition_2)
        serializer = ReservationSerializer(reservations, many=True)
        reservation_data = serializer.data
        
        # Get list of car ids which are reserved on the given date.
        occupied_car_id_lists = []
        for i in range(len(reservation_data)):
            occupied_car_id_lists.append(reservation_data[i]['car'])
        list_of_car_id = list(set(occupied_car_id_lists))
        
        # Setting availability of all car to True
        Car.objects.all().update(availability=True)
        
        # Setting availability of all reserved car to False
        for car_id in list_of_car_id:
            Car.objects.filter(id=car_id).update(availability=False)

        # Querying and filtering the cars based on various fields.
        cars = Car.objects.all()
        filters = {'model':model, 'seating_capacity':capacity, 'availability':availability}
        for key, value in filters.items():
            if value is not None:
                cars = cars.filter(**{key: value})
        car_serializer = AvailableCarSerializer(cars, many=True)

        return Response(car_serializer.data)
