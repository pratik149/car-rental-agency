import json
from datetime import date

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from car_api.models import Reservation
from car_api.serializers import ReservationSerializer


@api_view(['GET'])
def view_all_reservations(request):
    if request.method == 'GET':
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_reservation_details(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


@api_view(['POST'])
def add_reservation(request):
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
            
        if serializer.is_valid():
            current_date = date.today()
            issue_date = serializer.validated_data['issue_date']
            return_date = serializer.validated_data['return_date']

            car = serializer.validated_data['car']
            reservations = Reservation.objects.all().filter(car=car.id)

            # Check if the issue_date of new reservation doesn't clash with any previous reservations
            for r in reservations:
                if r.issue_date <= issue_date <= r.return_date:
                    content = {"message":"The selected car is not available on this date"}
                    return Response(data=json.dumps(content), status=status.HTTP_400_BAD_REQUEST)

            # Check whether issue_date is not some old date, and is less equal to return_date
            if current_date <= issue_date and issue_date <= return_date:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_reservation_details(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ReservationSerializer(reservation, data=request.data)

        if serializer.is_valid():
            current_date = date.today()
            issue_date = serializer.validated_data['issue_date']
            return_date = serializer.validated_data['return_date']

            car = serializer.validated_data['car']
            reservations = Reservation.objects.all().filter(car=car.id)

            # Check if the return_date of new reservation doesn't clash with any previous reservations
            for r in reservations:
                if r.issue_date <= return_date <= r.return_date:
                    res = {"message":"Failed to extend the date. Car is not available."}
                    return Response(data=json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

            if current_date <= issue_date and issue_date <= return_date:
                serializer.save()
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancel_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
