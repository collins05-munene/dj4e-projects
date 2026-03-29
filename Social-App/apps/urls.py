from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('create/account', views.CustomRegistrationView.as_view(), name='create-user'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('client/page', views.ClientPage.as_view(), name='client-page'),
    path('account/delete/', views.ClientDeleteView.as_view(), name='delete-account'),
    path('update/client/', views.ClientUpdateView.as_view(), name='update-client'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('post/create/', views.PostCreateView.as_view(), name='create-post'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add-comment'),
    path('posts/<int:pk>/details/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', views.ToggleLikeView.as_view(), name='toggle-like')
]