from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Player, Coach
# Create your views here.
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
            if hasattr(user, 'player'):
                return redirect('player-page')
            elif hasattr(user, 'coach'):
                return redirect("coach-page")
            elif user.is_staff:
                return redirect("admin-page")
        else:
            context = {
                "error": "Invalid Credentials"
            }
            return render(request, 'apps/login.html', context)

class AdminPage(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return render(self.request, 'apps/login.html')
    
    def get(self, request):
        players = Player.objects.all()
        
        context = {
            'players': players
        }
        return render(request, 'apps/admin.html', context)

        

