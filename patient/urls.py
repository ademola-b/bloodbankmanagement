from django.urls import path
from . import views

app_name = 'patient'
urlpatterns = [
    path('', views.homepage, name='index'),
    path('make-request/<int:id>/', views.MakeRequestFormView.as_view(), name='make_request'),
    path('request-history/', views.RequestHistory.as_view(), name='request_history'),
    path('available-blood/', views.AvailableBlood.as_view(), name='available_blood'),
    path('delete-request/<int:pk>/delete/', views.DeleteRequest.as_view(), name="delete_request"),
]
