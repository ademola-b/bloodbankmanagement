from datetime import datetime, timedelta
from datetime import date
from random import choice, shuffle
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
# from django.views import View
from django.views.generic import View, ListView
from blood.models import BloodRequest, BloodDonateTest
from . forms import DonateBloodForm, DonorForm
from . models import Donor, BloodDonate

# Create your views here.
# @login_required
def _application_no():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    appl = ['D', 'O', 'N', '-']

    [appl.append(choice(letters)) for _ in range(3)]
    [appl.append(choice(numbers)) for _ in range(3)]

    shuffle(list(appl))
    application_id = ''.join(appl)

    return application_id


def generate_appl_no():
    exists = True
    appl = None
    while exists:
        appl = _application_no()
        if not BloodDonateTest.objects.filter(application_id=appl).exists():
            exists = False
    return appl

class HomePageView(View):
    def get(self, request):
        form = DonorForm
        # try:
        #     donor = Donor.objects.get(user=request.user.id)
        #     user = request.user.id
        # except Donor.DoesNotExist:
        #     messages.warning(request, 'Account not found')
        #     return redirect('accts:login')

        return render(request, 'blood/dashboard.html', {'form':form})
    
    def post(self, request):
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            formData = form.save(commit=False)
            formData.user = request.user
            
            # check if user has account first
            def test_d(user=None):
                check_record = BloodDonateTest.objects.filter(donor = user).order_by('-test_date')
                # print(f"hee: {check_record}")

                daily_tests = BloodDonateTest.objects.filter(test_date = datetime.now())

                if not len(daily_tests) > 50:
                    if check_record:
                        future_date = check_record[0].test_date.date() + timedelta(days=15)
                        print(f"date:  {future_date}")
                        print(f"today date:  {datetime.now().date()}")

                        if datetime.now().date() > future_date:
                            BloodDonateTest.objects.create(
                                donor = user,
                                application_id = generate_appl_no(),
                                request_date = datetime.now(),
                                test_date = datetime.now() + timedelta(days=10), #get a week after
                                status = 'pending' 
                            )
                        else:
                            messages.warning(request, "You can only make a donation request after 2 weeks")
                    else:
                        BloodDonateTest.objects.create(
                            donor = user,
                            application_id = generate_appl_no(),
                            request_date = datetime.now(),
                            test_date = datetime.now() + timedelta(days=10), #get a week after
                            status = 'pending' 
                        )
                else:
                    messages.warning(request, "Daily limit for tests exhausted, try again tomorrow")
                      
            try:
                user = Donor.objects.get(user = request.user)
                test_d(user)
            except:
                dob = form.cleaned_data.get('age')
                today = date.today()
                date_format = "%Y-%m-%dT%H:%M"
                dob = datetime.strptime(dob, date_format).date()
                print(f"date type: {type(dob)}")
                print(f"date: {dob}")

                age = today.year - dob.year
                print(f"age:x {age}")
                if age < 18:
                    messages.warning(request, "You are below the age to donate blood. Minimum age is 18")
                    return redirect('donor:index')
                elif age >=75:
                    messages.warning(request, "You are above the age to donate blood. Highest age is 75")
                    return redirect('donor:index')
                else:
                    formData.save()

                    test_d(user=formData)

            messages.success(request, "You have been scheduled for test, kindly check your donation history to see the date.")
            return redirect('donor:index')
        else:
            messages.warning(request, f"{form.errors.as_text()}")

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
    model = BloodDonateTest
    template_name = 'donor/donate_history.html'
    context_object_name = 'donations'

    def get_success_url(self):
        return reverse("donor:index")

    def get_queryset(self):

        don = Donor.objects.get(user = self.request.user)
        donor_history = self.model.objects.filter(donor = don)
        return donor_history
        

    def get(self, request, *args, **kwargs):

        try:
            return super().get(request, *args, **kwargs)
        except Donor.DoesNotExist:
            messages.warning(self.request, "You don't have any donation history.")
            return redirect('donor:index')
        pass

