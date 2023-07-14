
from datetime import date, datetime, timedelta
from django import forms
from blood.models import BloodDonateTest
from . models import Donor, BloodDonate


class DonorForm(forms.ModelForm):
    age = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'age','class':'form-control', 'type': 'datetime-local', 'style': 'font-size: 15px'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'address','class':'form-control', 'placeholder':'Enter Address', 'style': 'font-size: 15px'}))
    gender = forms.ChoiceField(choices=[('male', 'male'), ('female', 'female')], widget=forms.Select(attrs={'id':'gender','class':'form-control select', 'style': 'font-size: 15px'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'id':'mobile','class':'form-control', 'placeholder':'Enter your phone no', 'style': 'font-size: 15px'}))
    profile_pic = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id':'profile_pic', 'name':"picture", 'class':'form-control', 'style': 'font-size: 15px'}))
    
    class Meta:
        model = Donor
        fields = ['age', 'gender', 'address','mobile','profile_pic']

    
    # def calculate_age(self, dob):
    #     today = date.today()
    #     print(f"{type(today.year)}")
    #     min = today.year - dob.year
    #     print(f"minu: {min}")
    #     return min
    
    # def clean_age(self):
    #     dob = self.cleaned_data['age']
    #     today = datetime.today().date()
    #     age = today.year - dob.year - ((today.month, today.day), (dob.month, dob.day))

    #     if age < 18:
    #         raise forms.ValidationError("Minimum age requirement is 18 years.")

    #     return dob

    # def clean_age(self):
    #     age = self.cleaned_data.get('age')
    #     # convert age to date time obj

    #     print(f"age ty: {type(age)}")

    #     datetime_format = "%Y-%m-%dT%H:%M"
    #     converted_age = datetime.strptime(str(age), datetime_format)
    #     print(f"age: {type(converted_age)}")
    #     print(f"age: {str(converted_age.year)}")


    #     dob = self.calculate_age(converted_age)
    #     print(f"dob:{dob}")
    #     if dob < 18:
    #         print(f"dob2:{dob}")
    #         return forms.ValidationError("Minimum Age is 18years")
    #     print("ssss")
    #     return age

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

