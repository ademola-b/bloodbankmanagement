from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from blood.models import BloodRequest
from . forms import DonateBloodForm
from . models import Donor, BloodDonate

# Create your views here.
@login_required
def homepage(request):
    try:
        donor = Donor.objects.get(user = request.user.id)
        user = request.user.id
    except:
        messages.warning(request, 'Account not found')
        return redirect('accts:login')

    dict = {
        'request_made': BloodRequest.objects.filter(request_by=request.user.id).count(),
        'pending_request': BloodRequest.objects.filter(request_by = request.user.id, status = 'pending').count(),
        'approved_request': BloodRequest.objects.filter(request_by=user, status='approved').count(),
        'rejected_request': BloodRequest.objects.filter(request_by=user, status='rejected').count(),

        'donation_made': BloodDonate.objects.all().filter(donor=donor).count(),
        'pending_donation': BloodDonate.objects.filter(donor = donor, status = 'pending').count(),
        'approved_donation':BloodDonate.objects.filter(donor=donor, status='approved').count(),
        'rejected_donation': BloodDonate.objects.filter(donor=donor, status='rejected').count(),
        }
    
    # print(dict['approved_donation'])
    
    return render(request, 'blood/dashboard.html', dict)

class DonateBloodFormView(LoginRequiredMixin, View):
    form_class = DonateBloodForm
    template_name = 'donor/donate_blood.html'
    
    def get(self, request):
        donor = Donor.objects.get(user = self.request.user)
        initial = {'bloodgroup': donor.bloodgroup, 'disease':'Nil'}
        form = self.form_class(initial)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        donor = Donor.objects.get(user = self.request.user)
        form = self.form_class(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.status = 'pending'
            don.donor = donor
            don.save()
            messages.success(request, "Blood Donate successful, Kindly wait for admin to approve")
            return redirect('donor:index')
        
        return render(request, self.template_name, {'form':form})
    
class DonateHistory(LoginRequiredMixin, ListView):
    model = BloodDonate
    template_name = 'donor/donate_history.html'
    context_object_name = 'donations'

    def get_queryset(self):
        return self.model.objects.filter(donor = self.request.user.donor)
    
