from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    name = models.CharField(max_length=30)
    TYPES = (
        ('Sedan', "Sedan"),
        ('SUV', "SUV"),
        ('WAGON', "WAGON")
    )
    Type = models.CharField(max_length=9,
                    choices=TYPES)
    year = models.DateField()
    def __str__(self):
        return self.name +' ' + self.Type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, id, state, lat, long, st, zip, short_name):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.state = state
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.short_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    dealership = models.IntegerField()
    purchase = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    review = models.CharField(max_length=300)
    purchase_date = models.DateField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_year = models.DateField()
    SENTIMENTS = (
        ('neutral', "neutral"),
        ('positive', "positive"),
        ('negative', "negative")
    )
    sentiment = models.CharField(max_length=9,
                    choices=SENTIMENTS) 
