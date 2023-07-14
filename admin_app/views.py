from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView, UpdateView
from django.shortcuts import render, redirect

from blood.models import BloodStock, BloodRequest, BloodDonateTest
from donor.models import Donor, BloodDonate
from patient.models import Patient

from . forms import UpdateTestResultForm

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
        # context['test_form'] = self.form_class()
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
    model = BloodDonateTest
    template_name = 'admin/donations.html'

    def get_queryset(self):
        return BloodDonateTest.objects.filter(status='approved')

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

class DonationRequests(LoginRequiredMixin, ListView):
    model = BloodDonateTest
    template_name = "admin/donation_requests.html"
    form_class = UpdateTestResultForm

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = UpdateTestResultForm()
        return context

class UpdateTestResult(LoginRequiredMixin, UpdateView):
    model = BloodDonateTest
    form_class = UpdateTestResultForm
    template_name = 'admin/update_test_result.html'
    success_message = "Donor's test has been updated, blood has also been donated"
    success_url = reverse_lazy('admin_page:donation_requests')

    def form_valid(self, form: BaseModelForm):

        print(f"request: {self.request.POST}")

        # perform the below only if has_surpassed return false
        if not self.object.has_surpassed:
            if self.object.status == 'pending':
                if 'reject_btn' in self.request.POST:
                    if self.object.reason == '':
                        messages.warning(self.request, "Kindly state reason why you are rejecting the blood")
                        return redirect('admin_page:update_test_result', self.object.test_id)
                    else:
                        donor = Donor.objects.get(id = self.object.donor.id)
                        donor.bloodgroup = self.object.blood_group
                        # save donor's bloodgroup
                        self.object.pint_amount = form.cleaned_data.get('pint_amount')
                        self.object.status = 'failed'
                        self.object.save()

                if 'approve' in self.request.POST:
                    self.object.status = 'approved'
                    stock = BloodStock.objects.get(bloodgroup = self.object.blood_group)
                    print(f"stock: {stock}")
                    stock.unit += self.object.pint_amount
                    stock.save()
                    self.object.save()
                    messages.success(self.request, f"Test Updated Successfully, {self.object.pint_amount} has been donated")
            elif self.object.status == 'approved':
                messages.warning(self.request, "Donation already made")
        else:
            messages.warning(self.request, "Test can't be updated, as donor missed his/her scheduled time")


        if not self.object.has_surpassed:
            print(f"sur: {self.object.has_surpassed}")
        else:
            messages.warning(self.request, "Test Date exceeded")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm):
        messages.warning(self.request, f"{form.errors.as_text()}")
        return self.render_to_response(self.get_context_data(form=form))

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



    

    

    
