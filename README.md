# Car-Rental-Agency
Task by ClinicSpots

## API hosted on:
https://car149.herokuapp.com/


# API endpoints according to tasks:

## Add new cars to the system, which could be used for renting
#### POST method: https://car149.herokuapp.com/car/add/
    Expects:
    {
      "vehicle_number": "8585",
      "model": "Etios",
      "seating_capacity": 5,
      "rent_per_day": 5000
    }

## Book an available car.
#### POST method: https://car149.herokuapp.com/rent/book/
    Expects:
    {
        "customer": 2,
        "car": 3,
        "issue_date": "2020-02-20",
        "return_date": "2020-02-22"
    }
    
## Show the details of a particular car with its availability and its currently active booking details if not available.
#### GET method: https://car149.herokuapp.com/car/<int:car_pk>/active_booking/
    Eg. https://car149.herokuapp.com/car/1/active_booking/
      
## Show the cars with their availability status on a given date. This API should have the feature to filter the cars based on various fields.
#### GET https://car149.herokuapp.com/car/status/?date=YYYY-MM-DD&model=STR&capacity=NUM&availability=BOOL
    Eg. https://car149.herokuapp.com/car/status/?date=2020-03-04
    Eg. https://car149.herokuapp.com/car/status/?model=Scorpio&capacity=8
    Eg. https://car149.herokuapp.com/car/status/?availability=True
         
## Extend the booking of the car, if the car is not already reserved for the dates user wants to extend the booking.
#### PUT method: https://car149.herokuapp.com/rent/<int:rent_pk>/extend/</i>
    Eg. https://car149.herokuapp.com/rent/3/extend/
    Expects:
    {
        "customer": 5,
        "car": 1,
        "issue_date": "2020-02-26",
        "return_date": "2020-02-30"
    }

## Cancel a specific Booking.
#### DELETE method: https://car149.herokuapp.com/rent/<int:rent_pk>/cancel/
    Eg. https://car149.herokuapp.com/rent/5/cancel/


## Other API endpoints:



