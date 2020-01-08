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
    trims = models.TextField(blank=True, null=True)
    bodystyles = models.ForeignKey(Bodystyle, blank=True, null=True, on_delete=models.PROTECT)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return self.name


class Listing(models.Model):
    name = models.TextField()
    uniqueID = models.TextField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField('USD', max_digits=15, decimal_places=2)
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)
    link = models.URLField()
    stateOrProvince = models.TextField(blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    engine = models.TextField(blank=True, null=True)
    transmission = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    sellerType = models.TextField(blank=True, null=True)
    car = models.ForeignKey(Car, null=True, related_name='listings', on_delete=models.PROTECT)

    def __unicode__(self):
        return u"%s" % self.name



