from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('create/account', views.CustomRegistrationView.as_view(), name='create-user'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('client/page', views.ClientPage.as_view(), name='client-page'),
    path('account/delete/', views.ClientDeleteView.as_view(), name='delete-account'),
    path('update/client/', views.ClientUpdateView.as_view(), name='update-client'),
  
]