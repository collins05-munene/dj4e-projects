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
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('create-category/',views.CreateCategory.as_view(), name='create-category'),
    path('update-category/<int:pk>/', views.UpdateCategory.as_view(), name='update-category'),
    path('add-to-cart/<int:item_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart-page/', views.CartView.as_view(), name='cart-page'),
    path('remove-item/<int:pk>/', views.DeleteCartView.as_view(), name='remove-item'),
    path('update-items/<int:pk>/', views.UpdateCartItem.as_view(), name='update-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout')
]