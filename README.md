# Car-Rental-Agency
Task by ClinicSpots

## API hosted on:
https://car149.herokuapp.com/


## API endpoints according to tasks:

#### Add new cars to the system, which could be used for renting
    POST:
    Desc: API to add new cars
    Live link: https://car149.herokuapp.com/car/add/
    Expects:
    {
      "vehicle_number": "8585",
      "model": "Etios",
      "seating_capacity": 5,
      "rent_per_day": 5000
    }

#### Book an available car.
    POST method:
    Live link: https://car149.herokuapp.com/rent/book/
    Expects:
    {
        "customer": 2,
        "car": 3,
        "issue_date": "2020-02-20",
        "return_date": "2020-02-22"
    }
    
#### Show the details of a particular car with its availability and its currently active booking details if not available.
    GET method:
    Format: https://car149.herokuapp.com/car/<int:car_pk>/active_booking/
    Live link: https://car149.herokuapp.com/car/1/active_booking/
      
#### Show the cars with their availability status on a given date. This API should have the feature to filter the cars based on various fields.
    GET method:
    Desc: Returns list of all cars with status on given date. When the date is not given then it takes today's date. User can filter by fields like model, seating_capacity, availability. 
    Format: https://car149.herokuapp.com/car/status/?date=YYYY-MM-DD&model=STR&capacity=NUM&availability=BOOL
    Live link 1: https://car149.herokuapp.com/car/status/?date=2020-03-04
    Live link 2: https://car149.herokuapp.com/car/status/?model=Scorpio&capacity=8
    Live link 3: https://car149.herokuapp.com/car/status/?availability=True
         
#### Extend the booking of the car, if the car is not already reserved for the dates user wants to extend the booking.
    PUT method:
    Desc: Extends the return date.
    Format: https://car149.herokuapp.com/rent/<int:rent_pk>/extend/
    Live link: https://car149.herokuapp.com/rent/3/extend/
    Expects:
    {
        "customer": 5,
        "car": 1,
        "issue_date": "2020-02-26",
        "return_date": "2020-02-30"
    }

#### Cancel a specific Booking.
    DELETE method: 
    Format: https://car149.herokuapp.com/rent/<int:rent_pk>/cancel/
    Live link: https://car149.herokuapp.com/rent/5/cancel/


## Other useful API endpoints:

### Customer
##### View all customer
    GET method:
    Link: https://car149.herokuapp.com/customer/
##### View particular customer details
    GET method:
    Format: https://car149.herokuapp.com/customer/<int:cust_pk>/
    link: https://car149.herokuapp.com/customer/2/
##### Add customer
    POST method:
    link: https://car149.herokuapp.com/customer/add/
    Expects:
    {
        "name": "Steven Holt",
        "email": "steven@gmail.com",
        "phone": "9855754754"
    }
 
### Car
##### View all cars
    GET method:
    Link: https://car149.herokuapp.com/customer/
##### View particular car details
    GET method:
    Format: https://car149.herokuapp.com/car/<int:car_pk>/
    link: https://car149.herokuapp.com/car/2/

### Reservation
##### View all reservations
    GET method:
    Link: https://car149.herokuapp.com/rent/
##### View particular reservation details
    GET method:
    Format: https://car149.herokuapp.com/rent/<int:rent_pk>/
    link: https://car149.herokuapp.com/rent/2/
