from django.urls import path
from . import views

app_name = 'blood'

urlpatterns = [
    path('', views.home_view, name='homepage')
]
