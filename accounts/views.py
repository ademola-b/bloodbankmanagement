from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect,render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View

from accounts.models import CustomUser
from donor.models import Donor
from donor.forms import DonorForm
from . forms import SignUpForm, DonorSignUpForm, LoginForm, PatientSignUpForm

# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'blood/signup.html'
    # success_url = reverse_lazy('accts:login')
    # error_message = 'Check field'

    def form_valid(self, form):
        # userform = SignUpForm()
        if self.request.method == 'POST':
            # donorForm = DonorForm(self.request.POST)
            print(form.cleaned_data['user_type'])
            user = form.save()
            # self.request.session['user'] = user.pk
            if form.cleaned_data['user_type'] == 'donor':
                self.request.session['user'] = user.pk
                messages.success(self.request, "Account successfully created, kindly login now")
                return redirect('accts:login')
            elif form.cleaned_data['user_type'] == 'patient':
                self.request.session['user'] = user.pk
                return redirect('accts:patient_complete_reg')
            else:
                messages.error(self.request, "Select an appropriate choice")
                return redirect('accts:sign_up')
            
        return super().form_valid(form)

    # def form_submit(self, request):
    #     if request.method == 'POST':
    #         form = SignUpForm(request.POST)
    #         if form.fields['user_type'] == 'Donor':
    #             donor = Donor.objects.create(user = )


    # def form_invalid(self, form):
    #     messages.error(self.request, self.error_message)
    #     return super().form_invalid(form)

class DonorCompleteReg(CreateView):
    form_class = DonorSignUpForm
    template_name = 'donor/complete_registration.html'
    # success_url = reverse_lazy('accts:login')

    def get(self, request):
        form = self.form_class()
        try:
            # form.fields['user'].queryset = CustomUser.objects.filter(id = request.session['user'])
            print(request.session['user'])
        except:
            messages.error(request, 'User not found')
            return redirect('accts:sign_up')
        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        # form.fields['user'].queryset = CustomUser.objects.filter(id = request.session['user'])
        if form.is_valid():
            user_data = get_user_model().objects.filter(id = request.session['user']).exists()
            if user_data:
                form = form.save(commit=False)
                form.user = get_user_model().objects.get(id=request.session['user'])
                form.save()
                messages.success(request, "Account successfully created, you can login now")
                return redirect('accts:login')
            else:
                messages.warning(request, "Account not found")
                return redirect('accts:sign_up')
        else:
            messages(request, "An error occurred")

        # if form.fields['user'].queryset:
        #     if form.is_valid():
        #         form.save()
        #         messages.success(request, "Account created successfully, Login now")
        #         return redirect('accts:login')
        # else:
        #     messages(request, "Account not found")
        #     return redirect('accts:sign_up')
        
        return render(request, self.template_name, {'form':form})

class PatientCompleteReg(CreateView):
    form_class = PatientSignUpForm
    template_name = 'patient/complete_registration.html'

    def get(self, request):
        form = self.form_class()        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        # form.fields['user'].queryset = CustomUser.objects.filter(id = request.session['user'])
        if form.is_valid():
            user_data = get_user_model().objects.filter(id = request.session['user']).exists()
            if user_data:
                form = form.save(commit=False)
                form.user = get_user_model().objects.get(id=request.session['user'])
                form.save()
                messages.success(request, "Account successfully created, you can login now")
                return redirect('accts:login')
            else:
                messages.warning(request, "Account not found")
                return redirect('accts:sign_up')
        else:
            messages(request, "An error occurred")
        
        return render(request, self.template_name, {'form':form})

class ProfileView(View):
    template_name = 'blood/profile.html'

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_staff:
                        return redirect('admin_page:index')
                    elif user.user_type == 'patient':
                        return redirect('patient:index')
                    elif user.user_type == 'donor':
                        return redirect('donor:index')
            else:
                print("Invalid username/password")
                messages.warning(request, "Invalid username/password")
        except Exception as e:
            print(e)
    
    form = LoginForm()
    return render(request, 'blood/login.html', {'form':form})
                

def logout_request(request):
    logout(request)
    return redirect('accts:login')