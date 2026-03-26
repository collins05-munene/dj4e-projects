from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import Client
from django.contrib.auth.models import User


# Create your views here.
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