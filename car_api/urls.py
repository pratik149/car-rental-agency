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
    path('car/status/<int:pk>/', car.view_car_details_active_booking), # API 3: Show details of car with booking details
    path('car/add/', car.add_car), # API 1: Add new cars
    path('car/update/<int:pk>/', car.edit_car_details),
    path('car/delete/<int:pk>/', car.delete_car),

    path('rent/', reservation.view_all_reservations),
    path('rent/<int:pk>/', reservation.view_reservation_details),
    path('rent/book/', reservation.book_car), # API 2: Book an available car
    path('rent/extend/<int:pk>/', reservation.extend_reservation_date), # API 5: Extend date of reservation.
    path('rent/cancel/<int:pk>/', reservation.cancel_reservation), # API 6: Cancel Specific booking

    path('car/status_date/', car.view_all_cars_on_given_date) # API 4: Show cars with availability status on given date.

]
