from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminPage.as_view(), name='admin-page'),
    path('login/', views.CustomLoginView.as_view(), name='login')
]