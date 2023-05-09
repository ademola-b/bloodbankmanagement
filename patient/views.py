from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
from blood.models import BloodRequest, BloodStock
from donor.models import BloodDonate, Donor
from . forms import MakeRequestForm
from . models import Patient

# Create your views here.

@login_required
def homepage(request):
    try:
        patient = Patient.objects.get(user = request.user.id)
        user = request.user.id
        bld = BloodStock.objects.filter(bloodgroup = patient.bloodgroup).aggregate(Sum('unit'))
    except:
        messages.warning(request, 'Account not found')
        return redirect('accts:login')

    dict = {
        'request_made': BloodRequest.objects.filter(request_by=request.user.id).count(),
        'pending_request': BloodRequest.objects.filter(request_by = user, status = 'pending').count(),
        'approved_request': BloodRequest.objects.filter(request_by = user, status='approved').count(),
        'rejected_request': BloodRequest.objects.filter(request_by = user, status='rejected').count(),
        'available_blood': bld['unit__sum'],
        }
    return render(request, 'blood/dashboard.html', dict)


class MakeRequestFormView(LoginRequiredMixin, View):
    form_class = MakeRequestForm
    template_name = 'patient/make_request.html'

    def get(self, request, id):
        blood = BloodStock.objects.get(id=id)
        # patient = Patient.objects.get(user=request.user.id)
        # mk = BloodRequest.objects.get(request_by=patient)
        # form = MakeRequestForm(instance=patient)
        form = self.form_class()
        # form.fields['patient_name'].initial = str(patient.user.first_name), str(patient.user.last_name)
        form.fields['bloodgroup'].initial = blood
        # form.fields['patient_age'].initial = patient.age
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, id):
        user = self.request.user
        blood = BloodStock.objects.get(id=id)
        form = self.form_class(request.POST)
        form.fields['bloodgroup'].initital = blood
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.bloodgroup
            patient = request.user
            # print(patient)
            blood_request.request_by = patient
            blood_request.save()
            messages.success(request, 'Blood successfully requested')
            if user.user_type == 'donor':
                return redirect('donor:index')
            elif user.user_type == 'patient':
                return redirect('patient:index')

        return render(request, self.template_name, {'form':form})

class RequestHistory(LoginRequiredMixin, ListView):
    login_url = "accounts:login"
    model = BloodRequest
    template_name = 'patient/request_history.html'
    context_object_name = 'requests'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(request_by = user)
    

class AvailableBlood(LoginRequiredMixin, ListView):
    model = BloodStock
    template_name = 'patient/available_blood.html'
    context_object_name = 'available_blood'

    def get_queryset(self):
        qs = super().get_queryset()
        # bld = BloodStock.objects.get(bloodgroup = patient.bloodgroup)
        user = self.request.user
        # print('user type: ', user.user_type)
        # print('User type: ',user.user_type)
        if user.user_type == 'donor':
            donor = Donor.objects.get(user = user)
            bld = BloodStock.objects.get(bloodgroup = donor.bloodgroup)
        elif user.user_type == 'patient':
            patient = Patient.objects.get(user = self.request.user)
            bld = BloodStock.objects.get(bloodgroup = patient.bloodgroup)

        # print(bld.bloodgroup)
        return bld
    
class DeleteRequest(LoginRequiredMixin, DeleteView):
    model = BloodRequest
    success_url = reverse_lazy('patient:request_history')
    