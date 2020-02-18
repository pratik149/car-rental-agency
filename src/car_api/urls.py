from django.urls import path
from car_api.views import car, reservation, customer

urlpatterns = [
    path('', car.home),

    path('customer/', customer.view_all_customers),
    path('customer/<int:pk>/', customer.view_customer_details),
    path('customer/add/', customer.add_customer),
    path('customer/update/<int:pk>/', customer.edit_customer_details),
    path('customer/delete/<int:pk>/', customer.delete_customer),

    path('car/', car.view_all_cars),
    path('car/<int:pk>/', car.view_car_details),
    path('car/add/', car.add_car),
    path('car/update/<int:pk>/', car.edit_car_details),
    path('car/delete/<int:pk>/', car.delete_car),

    path('reservation/', reservation.view_all_reservations),
    path('reservation/<int:pk>/', reservation.view_reservation_details),
    path('reservation/add/', reservation.add_reservation),
    path('reservation/update/<int:pk>/', reservation.edit_reservation_details),
    path('reservation/delete/<int:pk>/', reservation.delete_reservation),
]
