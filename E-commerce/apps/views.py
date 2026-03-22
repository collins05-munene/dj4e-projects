from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
from .models import Item, Client, Admin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import ClientRegistrationForm, ItemUpdateForm, ItemCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

# Create your views here.
class Homepage(View):
    def get(self, request):
        items = Item.objects.all()
        context = {'items': items}
        return render(request, 'apps/homepage.html', context)
    
class CustomRegistrationView(View):
    def get(self, request):
        form = ClientRegistrationForm()
        context = {'form': form}
        return render(request, 'apps/register.html', context)
    
    def post(self, request):
        form = ClientRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, f'Password mismacth')
                return redirect('register-client')
        
            if User.objects.filter(username=username).exists():
                messages.error(request, f'User {username} already exists.')
                return redirect('register-client')
            
            user = User.objects.create_user(username=form.cleaned_data['username'])
            user.set_password(password)
            user.save()

            client = form.save(commit=False)
            client.user = user
            client.save()

            return redirect('login')
        context = {'form': form}
        return render(request, 'apps/register.html', context)
    
class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'apps/login.html', context)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin-page')
            elif hasattr(user, 'client'):
                return redirect('client-page')
            
        else:
            context = {
                'error': "Invalid Credentials"
            }
            return render(request, 'apps/login.html', context)
    
class ClientPage(LoginRequiredMixin, View):
    def get(self, request):
        client = request.user.client
        items = Item.objects.all()
        context = {'client': client, 'items': items}
        return render(request, 'apps/client-page.html', context)
    
class AdminPage(LoginRequiredMixin, View):
    def get(self, request):
        items = Item.objects.all()
        clients = Client.objects.all()
       
        context = { 'clients': clients, "items": items}
        return render(request, 'apps/admin.html', context)

class UpdateItem(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return render(self.request, 'apps/not-authorized.html')
    
    model = Item
    form_class = ItemUpdateForm
    template_name = 'apps/update-item.html'
    success_url = reverse_lazy('admin-page')

class DeleteItem(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return render(self.request, 'apps/not-authorized.html')
    
    model = Item
    template_name = 'apps/delete-item.html'
    success_url = reverse_lazy('admin-page')
    pk_url_kwarg = 'id'

class CreateItem(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return render(self.request, 'apps/not-authorized.html')
    
    def get(self, request):
        form = ItemCreationForm()
        context = {'form': form}
        return render(request, 'apps/create-item.html', context)
    
    def post(self, request):
        form = ItemCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Item created successfully')
            return redirect('admin-page')
        
        context = {'form': form}
        return render(request, 'apps/create-item.html', context)

