from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('create-account', views.CustomRegistrationView.as_view(), name='create-user'),
    
]