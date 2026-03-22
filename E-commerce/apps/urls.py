from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns =[
    path('', views.Homepage.as_view(), name='homepage'),
    path('register-account/', views.CustomRegistrationView.as_view(), name='register-client'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('admin-page/', views.AdminPage.as_view(), name="admin-page"),
    path('client-page/', views.ClientPage.as_view(), name='client-page'),
    path('update-item/<int:pk>/', views.UpdateItem.as_view(), name='update-item'),
    path('delete-item/<int:id>/', views.DeleteItem.as_view(), name='delete-item'),
    path('create-item/', views.CreateItem.as_view(), name='create-item'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout')
]