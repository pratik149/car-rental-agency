from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from car_api.models import Customer
from car_api.serializers import CustomerSerializer


@api_view(['GET'])
def view_all_customers(request):
    """
    API endpoint to show all customer details.
    """
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_customer_details(request, cust_pk):
    """
    API endpoint to show a specific customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


@api_view(['POST'])
def add_customer(request):
    """
    API endpoint to add customer.
    """
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_customer_details(request, cust_pk):
    """
    API endpint to edit a specific customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_customer(request, cust_pk):
    """
    API endpoint for deleting customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
