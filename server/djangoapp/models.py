from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    maker = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealerId = models.IntegerField()
    year = models.DateField(null=True)
    COMPACT = 'compact'
    SEDAN = 'sedan'
    COUPE = 'coupe'
    HATCHBACK = 'hatchback'
    CONVERTIBLE = 'convertible'
    SPORTS_CAR = 'sports_car'
    SUV = 'suv'
    WAGON = 'wagon'
    MINIVAN = 'minivan'
    PICKUP_TRUCK = 'pickup_truck'
    TYPEOFCAR_CHOICES = [
        (COMPACT, 'Compact'),
        (SEDAN, 'Sedan'),
        (COUPE, 'Coupe'),
        (HATCHBACK, 'Hatchback'),
        (CONVERTIBLE, 'Convertible'),
        (SPORTS_CAR, 'Sports Car'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon'),
        (MINIVAN, 'Minivan'),
        (PICKUP_TRUCK, 'Pickup Truck')
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPEOFCAR_CHOICES,
        default=SEDAN
    )

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Year: " + str(self.year.year) + "," + \
               "Type: " + self.type + "," + \
               "Maker: " + self.maker.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
