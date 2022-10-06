from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - DescriptionAdd
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250)
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
    make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=[
        ('SEV','Sedan'),
        ('SUD','SUV'),
        ('VAN','VAN'),
        ('WAG','WAGON'),
        ('CON','CONVERTABLE'),
    ])
    year = models.DateField()
    def __str__(self):
        return f'{self.year} {self.name}'

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long,  short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip
    def __str__(self):
        return 'Dealer name: ' + self.full_name
class DealerReview:
    def __init__(self, dealership, name, purchase, review, sentiment, id, purchase_date=None, car_make=None, car_model=None, car_year=None):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    def __str__(self):
        return 'Review text: ' + self.review

# <HINT> Create a plain Python class `DealerReview` to hold review data
