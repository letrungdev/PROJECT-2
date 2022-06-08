from django.db import models
from datetime import datetime, timedelta


class Billfold(models.Model):
    user = models.CharField(max_length=20)
    billfold_name = models.CharField(max_length=30, null=True)
    currency_unit = models.CharField(max_length=20, null=True)
    balance = models.CharField(max_length=20, null=True)
    inflow = models.CharField(max_length=20, null=True)
    outflow = models.CharField(max_length=20, null=True)


class Expenditureplan(models.Model):
    category = models.CharField(max_length=40, null=True)
    amount = models.CharField(max_length=40, null=True)


class Transaction(models.Model):
    user = models.CharField(max_length=30, null=True)
    amount = models.CharField(max_length=40, null=True)
    category = models.CharField(max_length=40, null=True)
    type = models.CharField(max_length=40, null=True)
    note = models.CharField(max_length=60, null=True)
    tran_time = models.CharField(max_length=30, null=True)
    tran_image = models.ImageField(null=True)


class Analysis(models.Model):
    content = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=30, null=True)



