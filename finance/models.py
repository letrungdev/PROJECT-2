from django.db import models
from datetime import datetime, timedelta


class Billfold(models.Model):
    user = models.CharField(max_length=20)
    balance = models.CharField(max_length=20)
    inflow = models.CharField(max_length=20)
    outflow = models.CharField(max_length=20)


class Expenditureplan(models.Model):
    category = models.CharField(max_length=40)
    amount = models.CharField(max_length=40)


class Transaction(models.Model):
    amount = models.CharField(max_length=40)
    category = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    note = models.CharField(max_length=60)




