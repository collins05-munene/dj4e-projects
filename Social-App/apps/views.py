from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegistrationForm, ClientUpdateForm, UserUpdateForm
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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


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
    
class ClientUpdateView(LoginRequiredMixin, View):
    template_name = 'apps/update-client.html'
    def get(self, request):
        client, _ = Client.objects.get_or_create(user=request.user)

        client_form = ClientUpdateForm(instance=client)
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        context = {
            'client_form': client_form,
            'user_form': user_form,
            'password_form': password_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        client, _ = Client.objects.get_or_create(user=request.user)

        client_form = ClientUpdateForm(request.POST, instance=client)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:
            if client_form.is_valid()  and user_form.is_valid():
                client_form.save()
                user_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('client-page')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) #Keep user logged in
                messages.success(request, "Password Updated successfully")
                return redirect('client-page')
        
        context = {
            'client_form': client_form,
            'user_form': user_form,
            'password_form': password_form
            }
        return render(request, self.template_name, context)