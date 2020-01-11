from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Bodystyle(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.TextField()
    make = models.TextField()
    years = models.TextField(blank=True, null=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    trims = models.TextField(blank=True, null=True)
    bodystyles = models.ForeignKey(Bodystyle, blank=True, null=True, on_delete=models.PROTECT)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)
    craigslist_searchterm = models.TextField()
    carscom_modelid = models.IntegerField()
    carscom_makeid = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return self.name


class Listing(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = MoneyField(max_digits=15, decimal_places=2, default_currency='USD')
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    date = models.DateTimeField(default=date.today)
    link = models.URLField()
    region = models.CharField(max_length=30, blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    engine = models.CharField(max_length=25, blank=True, null=True)
    transmission = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    seller_type = models.CharField(max_length=15, blank=True, null=True)
    vin = models.CharField(max_length=17, blank=True, null=True)
    car = models.ForeignKey(Car, null=True, related_name='listings', on_delete=models.PROTECT)
    other_info = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return self.name



