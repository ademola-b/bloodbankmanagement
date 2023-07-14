from django.contrib import admin
from . models import BloodRequest, BloodStock, BloodDonateTest

# Register your models here.
admin.site.register(BloodRequest)
admin.site.register(BloodStock)
admin.site.register(BloodDonateTest)