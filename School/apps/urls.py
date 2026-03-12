from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminPage.as_view(), name='admin-page'),
    path('/create-student/', views.CreateStudent.as_view(), name='create-student'),
    path('/update-student/<int:adm>/', views.UpdateStudent.as_view(), name='update-student'),
    path('delete-student/<int:adm>/', views.StudentDeleteView.as_view(), name='delete-student'),
    path('teacher-details/', views.TeacherDetails.as_view(), name="teacher-details"),
    path('create-teacher/', views.CreateTeacher.as_view(), name='create-teacher'),
]