from django.urls import path
from car_api.views import customer, car, reservation

urlpatterns = [
    path('', car.home),

    path('customer/', customer.view_all_customers),
    path('customer/add/', customer.add_customer),
    path('customer/<int:cust_pk>/', customer.view_customer_details),
    path('customer/<int:cust_pk>/update/', customer.edit_customer_details),
    path('customer/<int:cust_pk>/delete/', customer.delete_customer),

    path('car/', car.view_all_cars),
    path('car/add/', car.add_car), # API 1: Add new cars
    path('car/<int:car_pk>/', car.view_car_details),
    path('car/<int:car_pk>/active_booking/', car.view_car_details_active_booking), # API 3: Show details of car with booking details
    path('car/<int:car_pk>/update/', car.edit_car_details),
    path('car/<int:car_pk>/delete/', car.delete_car),

    path('rent/', reservation.view_all_reservations),
    path('rent/book/', reservation.book_car), # API 2: Book an available car
    path('rent/<int:rent_pk>/', reservation.view_reservation_details),
    path('rent/<int:rent_pk>/extend/', reservation.extend_reservation_date), # API 5: Extend date of reservation.
    path('rent/<int:rent_pk>/cancel/', reservation.cancel_reservation), # API 6: Cancel Specific booking

    path('car/status/', car.view_all_cars_on_given_date) # API 4: Show cars with availability status on given date.

]
