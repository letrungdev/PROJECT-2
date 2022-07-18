from django.db import models
from datetime import datetime, timedelta


class Billfold(models.Model):
    user = models.CharField(max_length=20)
    billfold_name = models.CharField(max_length=30, null=True)
    currency_unit = models.CharField(max_length=20, null=True)
    balance = models.IntegerField(null=True)


class Transaction(models.Model):
    user = models.CharField(max_length=30, null=True)
    amount = models.IntegerField(null=True)
    category = models.CharField(max_length=40, null=True)
    kind = models.CharField(max_length=40, null=True)
    type = models.CharField(max_length=40, null=True)
    note = models.CharField(max_length=60, null=True)
    tran_time = models.CharField(max_length=30, null=True)
    tran_image = models.ImageField(null=True)


class Track(models.Model):
    user = models.CharField(max_length=30, null=True)
    billfold = models.CharField(max_length=30, null=True)
    inflow = models.CharField(max_length=20, null=True)
    outflow = models.CharField(max_length=20, null=True)
    balance = models.CharField(max_length=30, null=True)
    time_track = models.CharField(max_length=30, null=True)


class Analysis(models.Model):
    user = models.CharField(max_length=30, null=True)
    interval = models.CharField(max_length=30, null=True)
    ratio = models.CharField(max_length=100, null=True)



