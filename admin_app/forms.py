from django import forms

from blood.models import BloodDonateTest

class UpdateTestResultForm(forms.ModelForm):

    blood_group_choice = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    blood_group = forms.ChoiceField(choices=blood_group_choice, widget=forms.Select(attrs={'id':'blood_group','class':'form-control select', 'style': 'font-size: 15px'}))
    pint_amount = forms.CharField(required=False, widget=forms.NumberInput(attrs={'id':'pint','class':'form-control', 'type':'number'}))
    reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'id': 'reason', 'class': 'form-control', 'placeholder':"Give Reasons on why you are rejecting the donor's blood", 'style': 'font-size: 15px'}))


    class Meta:
        model = BloodDonateTest
        fields = [
            'blood_group',
            'pint_amount',
            'reason'
        ]
 
    def clean_pint_amount(self):
        pint = self.cleaned_data.get('pint_amount')
        if pint is not None:
            print(f"type: {type(pint)}")
            if int(pint) > 500:
                print("heeee")
                raise forms.ValidationError("The maximum pint a donor can donate is 500ml")
        return pint