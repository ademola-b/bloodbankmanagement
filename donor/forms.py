from django import forms
from . models import Donor, BloodDonate

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['bloodgroup','address','mobile','profile_pic']

class DonateBloodForm(forms.ModelForm):
    # bloodgroup = forms.ModelChoiceField(queryset=Donor.objects.none(), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = BloodDonate
        fields = ['disease', 'bloodgroup', 'unit']

        widgets = {
            'disease':forms.TextInput(attrs={'class':'form-control',}),
            'age':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}), 
            'bloodgroup':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),  
            'unit':forms.TextInput(attrs={'class': 'form-control'})    
        }
        