from django.urls import path

from . import views

app_name = 'admin_page'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('blood-stock/', views.BloodStockView.as_view(), name='blood_stock'),
    path('donors/', views.DonorsView.as_view(), name='donors'),
    path('donors/delete/<int:pk>/', views.DonorDelete.as_view(), name='delete_donor'),
    path('patients/', views.PatientsView.as_view(), name='patients'),
    path('patients/delete/<int:pk>/', views.PatientDelete.as_view(), name='delete_patient'),
    path('donation-requests/', views.DonationRequests.as_view(), name='donation_requests'),
    path('donation-requests/test-update/<str:pk>/', views.UpdateTestResult.as_view(), name='update_test_result'),
   
   
   
   
    path('donations/', views.Donations.as_view(), name='donations'),
    path('approve-donation/<int:pk>/', views.approve_donation, name='approve_donation'),
    path('reject-donation/<int:pk>/', views.reject_donation, name='reject_donation'),
    path('rollback-donation/<int:pk>/', views.rollback_donation, name='rollback_donation'),
    path('requests/', views.Requests.as_view(), name="requests"),
    path('approve-request/<int:pk>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:pk>/', views.reject_request, name='reject_request'),
    path('rollback-request/<int:pk>/', views.rollback_request, name='rollback_request'),
]
