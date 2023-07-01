from django.urls import path
from . import views

app_name = 'accts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.login_request, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('donor-complete-registration/', views.DonorCompleteReg.as_view(), name='donor_complete_reg'),
    path('patient-complete-registration/', views.PatientCompleteReg.as_view(), name='patient_complete_reg'),
]
