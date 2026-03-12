from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.AdminPage.as_view(), name='admin-page'),
    path('create-student/', views.CreateStudent.as_view(), name='create-student'),
    path('update-student/<int:adm>/', views.UpdateStudent.as_view(), name='update-student'),
    path('delete-student/<int:adm>/', views.StudentDeleteView.as_view(), name='delete-student'),
    path('teacher-details/', views.TeacherDetails.as_view(), name="teacher-details"),
    path('create-teacher/', views.CreateTeacher.as_view(), name='create-teacher'),
    path("update-teacher/<int:id>/", views.UpdateTeacher.as_view(), name='update-teacher'),
    path('delete-teacher/<int:id>/', views.TeacherDeleteView.as_view(), name='delete-teacher'),
    path('teacher-dashboard/', views.TeacherDashboard.as_view(), name='teacher-dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]