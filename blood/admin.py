from django.contrib import admin
from . models import BloodRequest, BloodStock

# Register your models here.
admin.site.register(BloodRequest)
admin.site.register(BloodStock)