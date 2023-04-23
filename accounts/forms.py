from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from blood.models import BloodStock
from donor.models import Donor
from patient.models import Patient

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    user_type = forms.ChoiceField(choices=[('donor', 'Donor'), ('patient','Patient')], 
                                  widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 
           'first_name',
           'last_name',
            'email', 
            'user_type',
            ]
        
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),           
        }

class DonorSignUpForm(forms.ModelForm):
    # user = forms.ModelChoiceField(queryset=get_user_model().objects.none(), empty_label=None)
    bloodgroup = forms.ModelChoiceField(queryset=BloodStock.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Donor
        fields = ['profile_pic', 'bloodgroup','address', 'mobile']

    # def __init__(self, *args, **kwargs):
    #     super(DonorSignUpForm, self).__init__(*args, **kwargs)

    #     self.fields['bloodgroup'].queryset = BloodStock.objects.all()
        


class PatientSignUpForm(forms.ModelForm):
    # user = forms.ModelChoiceField(queryset=get_user_model().objects.none(), empty_label=None)
    bloodgroup = forms.ModelChoiceField(queryset=BloodStock.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['user']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'username','class':'form-control', 'placeholder':'Enter your username', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'password','class':'form-control', 'placeholder':'***********'}))