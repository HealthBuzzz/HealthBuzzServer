from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, 
                             on_delete=models.CASCADE,
                             related_name='profile')
    today_stretching_count = models.IntegerField(default=0)
    today_water_count = models.IntegerField(default=0)
    today_ranking_stretch = models.IntegerField(default=100)
    today_ranking_water = models.IntegerField(default=100)

class DailyStretching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_stretching')
    hour = models.IntegerField()
    minute = models.IntegerField()
    
class DailyWater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_water')
    hour = models.IntegerField()
    minute = models.IntegerField()
    amount = models.IntegerField()
    
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

