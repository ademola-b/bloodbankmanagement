import uuid
import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from patient.models import Patient
from donor.models import Donor

class BloodStock(models.Model):
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    request_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    # request_by_donor = models.ForeignKey(Donor, null=True, on_delete=models.CASCADE)
    # patient_name = models.CharField(max_length=30)
    # patient_age = models.PositiveIntegerField()
    reason = models.CharField(max_length=500)
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default = "pending")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format(self.request_by, self.bloodgroup) 


test_choices = [
    # ('not scheduled', 'pending'),
    ('pending', 'pending'),
    ('failed', 'failed'),
    ('approved', 'approved')
]

class BloodDonateTest(models.Model):
    test_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    application_id = models.CharField(max_length=30)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now=True)
    test_date = models.DateTimeField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    pint_amount = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=test_choices, default='pending')
    has_surpassed = models.BooleanField()
    reason = models.CharField(max_length=1000, null=True, blank=True)

    @property
    def has_surpassed(self):
        if timezone.now() > self.test_date:
            return True
        return False
    
    def __str__(self):
        return f"{self.donor.user.first_name}"
        