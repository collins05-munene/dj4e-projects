from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('admin', views.AdminPage.as_view(), name='admin-page'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('create-coach/', views.CreateCoach.as_view(), name='create-coach'),
    path('coach-page', views.CoachPage.as_view(), name="coach-page"),
    path('create-player', views.CreatePlayer.as_view(), name='create-player')
]