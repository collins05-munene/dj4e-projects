from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Player, Coach
from django.contrib import messages
from .forms import ContractForm, PlayerForm
from django.db import transaction
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
            if user.is_staff:
                return redirect("admin-page")
            elif hasattr(user, 'player'):
                return redirect('player-page')
            elif hasattr(user, 'coach'):
                return redirect("coach-page")
           
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
        coaches = Coach.objects.all()
        
        context = {
            'players': players, 'coaches': coaches
        }
        return render(request, 'apps/admin.html', context)

class Homepage(View):
    def get(self, request):
        return render(request, 'apps/homepage.html')
    
class CoachPage(View):
    def get(self, request):
        coaches = Coach.objects.all()
        context = {'coaches': coaches}

        return render(request, 'apps/coach-page.html', context)


class CreateCoach(View):
    def get(self, request):
        coaches = Coach.objects.all()
        context = {'coaches': coaches}

        return render(request, 'apps/create-coach.html', context)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get("phone")
        id_no = request.POST.get('id_no')
        date_of_birth = request.POST.get('dob')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("create-coach")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect("create-coach")
        
        user = User.objects.create_user(username=username,password=password)

        coach = Coach.objects.create(user=user, name=name, email=email, phone_number=phone_number, id_no=id_no, date_of_birth=date_of_birth)

        messages.success(request, f"Coach {name} registered successfully")
        return redirect("login")

class CreatePlayer(View):
    def get(self, request):
        context = {'player_form': PlayerForm(), 'contract_form': ContractForm()}
        return render(request, 'apps/create-player.html', context)
    
    def post(self, request):
        player_form = PlayerForm(request.POST)
        contract_form = ContractForm(request.POST)

        if player_form.is_valid() and contract_form.is_valid():
            try:
                with transaction.atomic():
                    contract = contract_form.save()
                    player = player_form.save(commit=False)
                    player.contract = contract
                    player.save()
                    player_form.save_m2m()
                return redirect('players-list')
            except Exception as e:
                context = {
                    'player_form': player_form,
                    'contract_form': contract_form,
                    'error': str(e)
                }
                return render(request, 'create-player.html', context) 
            
        context = {'player_form': player_form, 'contract_form': contract_form}
        return render(request, 'apps/create-player.html', context)             
