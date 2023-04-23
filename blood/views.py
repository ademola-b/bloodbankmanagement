from django.shortcuts import render
from django.views.generic import View
from . models import BloodStock
# Create your views here.
def home_view(request):
    
    stock = BloodStock.objects.all()
    # print(stock)

    #check if any blood group is available in the db, add if no blood
    if len(stock) == 0:
        blood1 = BloodStock()
        blood1.bloodgroup = "A+"
        blood1.save()

        blood2 = BloodStock()
        blood2.bloodgroup = "A-"
        blood2.save()

        blood3 = BloodStock()
        blood3.bloodgroup = "B+"
        blood3.save()        

        blood4 = BloodStock()
        blood4.bloodgroup = "B-"
        blood4.save()

        blood5 = BloodStock()
        blood5.bloodgroup = "AB+"
        blood5.save()

        blood6 = BloodStock()
        blood6.bloodgroup = "AB-"
        blood6.save()

        blood7 = BloodStock()
        blood7.bloodgroup = "O+"
        blood7.save()

        blood8 = BloodStock()
        blood8.bloodgroup = "O-"
        blood8.save()

        print('Blood Added')

    return render(request, 'blood/homepage.html', context={})

