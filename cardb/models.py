from djmoney.models.fields import MoneyField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Bodystyle(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.TextField()
    make = models.TextField()
    start_year = models.IntegerField(blank=True)
    end_year = models.IntegerField(blank=True)
    trims = models.TextField(blank=True)
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

    def get_absolute_url(self):
        return reverse('car-detail', args=[str(self.id)])


class Listing(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = MoneyField(max_digits=15, decimal_places=2, default_currency='USD')
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    date = models.DateTimeField(default=date.today)
    link = models.URLField()
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=50, blank=True)
    mileage = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    engine = models.CharField(max_length=25, blank=True)
    transmission = models.CharField(max_length=15, blank=True)
    title = models.CharField(max_length=10, blank=True)
    seller_type = models.CharField(max_length=15, blank=True)
    vin = models.CharField(max_length=17, blank=True)
    car = models.ForeignKey('Car', null=True, on_delete=models.PROTECT)
    other_info = models.TextField(blank=True)
    source = models.CharField(max_length=20)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return self.name



