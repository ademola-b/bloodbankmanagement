from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
from django.shortcuts import render, redirect

from blood.models import BloodStock, BloodRequest
from donor.models import Donor, BloodDonate
from patient.models import Patient

# Create your views here.

class HomePageView(ListView):
    model = BloodStock
    template_name = 'admin/dashboard.html'
    context_object_name = 'requests'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bld = BloodStock.objects.all().aggregate(Sum('unit'))
        context["requests_made"] = BloodRequest.objects.all().count()
        context["pending_request"] = BloodRequest.objects.filter(status='pending').count()
        context["approved_requests"] = BloodRequest.objects.filter(status='approved').count()
        context["rejected_requests"] = BloodRequest.objects.filter(status='rejected').count()
        context["donations_made"] = BloodDonate.objects.all().count()
        context["pending_donations"] = BloodDonate.objects.filter(status='pending').count()
        context["approved_donations"] = BloodDonate.objects.filter(status='approved').count()
        context["rejected_donations"] = BloodDonate.objects.filter(status='rejected').count()
        context["bld"] = bld['unit__sum']
        # print(context)
        return context
    

class BloodStockView(LoginRequiredMixin, ListView):
    model = BloodStock
    template_name = 'admin/blood_stock.html'
    context_object_name = 'blood'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bld = BloodStock.objects.all().aggregate(Sum('unit'))
        context["bld"] = bld['unit__sum']
        # print(context)
        return context
    
class DonorsView(LoginRequiredMixin, ListView):
    model = Donor
    template_name = 'admin/donors.html'
    context_object_name = 'donors'

class DonorDelete(SuccessMessageMixin, DeleteView):
    model = Donor
    success_message = "Donor Successfully Deleted"
    success_url = reverse_lazy("admin_page:donors")
    

class PatientsView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'admin/patients.html'
    context_object_name = 'patients'

class PatientDelete(SuccessMessageMixin, DeleteView):
    model = Patient
    success_message = "Patient Successfully deleted"
    success_url = reverse_lazy("admin_page:patients")
    

class Donations(LoginRequiredMixin, ListView):
    model = BloodDonate
    template_name = 'admin/donations.html'
    context_object_name = 'donations'

@login_required
def approve_donation(request, pk):
    #get necessary data
    donation = BloodDonate.objects.get(id=pk)
    blood_group = donation.bloodgroup
    unit = donation.unit

    stock = BloodStock.objects.get(bloodgroup = blood_group)
    stock.unit += unit
    stock.save()

    donation.status = 'approved'
    messages.success(request, 'Donation approved')
    donation.save()
    return redirect('admin_page:donations')

@login_required
def reject_donation(request, pk):
    #get necessary data
    donation = BloodDonate.objects.get(id=pk)
    donation.status = 'rejected'
    messages.warning(request, 'Donation rejected')
    donation.save()
    return redirect('admin_page:donations')

class Requests(LoginRequiredMixin, ListView):
    model = BloodRequest
    template_name = 'admin/requests.html'
    context_object_name = 'requests'

    # def get_queryset(self):
    #     req = BloodRequest.objects.filter(status = 'pending')
    #     return req

@login_required
def rollback_donation(request, pk):
    don = BloodDonate.objects.get(id=pk)
    bloodgroup = don.bloodgroup
    unit = don.unit
    status = don.status
    stock = BloodStock.objects.get(bloodgroup = bloodgroup)
    if status == 'approved':
        stock.unit -= unit
        stock.save()
        messages.info(request, "Rollback successful")
        don.status = 'pending'
    elif status == 'rejected':
        don.status = 'pending'
        messages.info(request, "Rollback successful")
    
    
    don.save()
    return redirect('admin_page:donations')

@login_required
def approve_request(request, pk):
    req = BloodRequest.objects.get(id=pk)
    bloodgroup = req.bloodgroup
    unit = req.unit
    stock = BloodStock.objects.get(bloodgroup = bloodgroup)
    #check if available unit is greater than the requested unit
    if stock.unit > unit:
        stock.unit -= unit
        messages.success(request, "Request successfully approve")
        stock.save()
        req.status = 'approved'
    else:
        messages.warning(request, "There's no enough blood to approve this request")
    req.save()

    return redirect('admin_page:requests')

@login_required
def reject_request(request, pk):
    req = BloodRequest.objects.get(id=pk)
    req.status = 'rejected'
    messages.warning(request, "Blood request rejected")
    req.save()
    return redirect("admin_page:requests")

@login_required
def rollback_request(request, pk):
    req = BloodRequest.objects.get(id=pk)
    bloodgroup = req.bloodgroup
    unit = req.unit
    status = req.status
    stock = BloodStock.objects.get(bloodgroup = bloodgroup)
    if status == 'approved':
        stock.unit += unit
        messages.success(request, "Request successfully rollbacked")
        stock.save()
        req.status = 'pending'
    elif status == 'rejected':
        req.status = 'pending'
        messages.success(request, "Request successfully rollbacked")
    
    req.save()
    return redirect("admin_page:requests")



    

    

    
