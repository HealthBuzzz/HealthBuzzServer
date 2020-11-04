from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class StretchingData(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField()

class WaterData(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_pk=instance.id)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
