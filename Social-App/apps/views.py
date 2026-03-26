from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import logout


# Create your views here.
User = get_user_model()

class Homepage(View):
    def get(self, request):
        return render(request, 'apps/home.html')
    
class CustomRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'apps/create-user.html', context)
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Password mismatch')
                return redirect('register-user')
            if User.objects.filter(username=username).exists():
                messages.error(request, f'{username} already exists')

            user = User.objects.create_user(username=form.cleaned_data['username'])
            user.set_password(password)
            user.save()

            client = form.save(commit=False)
            client.user = user
            client.save()

            return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'apps/create-user.html', context)
    

class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'apps/login.html', context)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            if user.is_active:
                return redirect('client-page')
        else:
            context = {
                'error': 'Invalid Credentials'
            }
            return render(request, 'apps/login.html', context)

class ClientPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'apps/client-page.html')
    
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'apps/delete-account.html'
    success_url = reverse_lazy('homepage')
    
    def get_object(self):
        return self.request.user
    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)