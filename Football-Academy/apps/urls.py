from django.urls import path
from . import views

app_name = 'apps'
urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('admin', views.AdminPage.as_view(), name='admin-page'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('create-coach/', views.CreateCoach.as_view(), name='create-coach'),
    path('coach-page', views.CoachPage.as_view(), name="coach-page"),
    path('register-player', views.RegisterPlayer.as_view(), name='register-player'),
    path('player-page/', views.PlayerPage.as_view(), name='player-page'),
    path('update/<int:pk>/', views.UpdatePlayer.as_view(), name='update-player'),
    path('update-coach/<int:pk>/', views.UpdateCoach.as_view(), name='update-coach'),
]