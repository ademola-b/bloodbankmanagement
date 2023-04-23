from django import forms
from blood.models import BloodRequest, BloodStock
from . models import Patient

class MakeRequestForm(forms.ModelForm):
    # bloodgroup = forms.ModelChoiceField(queryset=BloodStock.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = BloodRequest
        fields = ['reason', 'bloodgroup', 'unit']

        widgets = {
            # 'patient_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Patient Name', 'readonly':'readonly'}),
            # 'patient_age':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Patient Age', 'readonly':'readonly'}), 
            'reason':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reason'}),  
            'bloodgroup':forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'})    
        }