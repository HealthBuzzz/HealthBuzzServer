from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StretchingData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    amount = models.IntegerField()

class WaterData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    amount = models.IntegerField()

