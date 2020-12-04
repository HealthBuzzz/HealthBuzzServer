from django.contrib import admin

# Register your models here.
from buzz.models import *

admin.site.register(Profile)
admin.site.register(DailyStretching)
admin.site.register(DailyWater)
admin.site.register(StretchingData)
admin.site.register(WaterData)
