from django.contrib import admin

# Register your models here.
from buzz.models import Profile, DailyStretching, DailyWater

admin.site.register(Profile)
admin.site.register(DailyStretching)
admin.site.register(DailyWater)
