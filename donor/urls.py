from django.urls import path
from . import views

app_name = 'donor'
urlpatterns = [
    path('', views.homepage, name='index'),
    path('donate-blood/', views.DonateBloodFormView.as_view(), name='donate_blood'),
    path('donation-history/', views.DonateHistory.as_view(), name='donation_history'),
    path('make-request/', views.DonateHistory.as_view(), name='donation_history'),
    
]
