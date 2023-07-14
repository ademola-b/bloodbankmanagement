from django.db import models
from django.contrib.auth import get_user_model

class Donor(models.Model):
    user=models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='donor')
    profile_pic= models.ImageField(upload_to='profile_pic/Donor/', null=True, blank=True)    
    bloodgroup=models.CharField(max_length=10, null=True, blank=True)
    age = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=8, choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], default='other')
    address = models.CharField(max_length=70)
    mobile = models.CharField(max_length=20, null=False)
   
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    
    @property
    def get_instance(self):
        return self
    
    def __str__(self):
        return self.user.first_name

class BloodDonate(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    disease=models.CharField(max_length=100,default="Nil")
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20, choices = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default="pending")
    date=models.DateField(auto_now=True)
    
    def __str__(self):
        return '{0} - {1}'.format(self.donor.user.first_name, self.bloodgroup)