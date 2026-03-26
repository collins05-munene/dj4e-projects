from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView, ListView
from .models import Item, Category, Cart, CartItem, Client, Admin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import ClientRegistrationForm, ItemUpdateForm, ItemCreationForm, CategoryCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
import base64
from datetime import datetime
import json
from django.http import JsonResponse

# Create your views here.
"""
def get_mpesa_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET
        )
    )
    return response.json().get('access-token')

def lipa_na_mpesa(phone_number, amount):
    access_token = get_mpesa_access_token()

    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    password = base64.b64encode(
        f'{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}'.encode().decode('utf-8')
    )
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': settings.MPESA_SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackUrl': settings.MPESA_CALLBACK_URL,
        'AccountReference': 'e-shop',
        'TransactionDesc': 'Payment'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
"""
class Homepage(View):
    def get(self, request):
        items = Item.objects.all()
        
        search_query = request.GET.get('search')
        if search_query:
            items = items.filter(
                Q(name__icontains=search_query)
                )
        category_filter = request.GET.get('category')
        if category_filter:
            items = items.filter(category_id=category_filter)

        context = {
            'items': items,
            'categories': Category.objects.all(),
            }
        return render(request, 'apps/homepage.html', context)
    
class CustomRegistrationView(View):
    def get(self, request):
        form = ClientRegistrationForm()
        context = {
            'form': form,
          
            }
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
    
class CreateCategory(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return render(self.request, 'apps/not-authorized.html')
    def get(self, request):
        form = CategoryCreationForm()
        context = {'form': form}
        return render(request, 'apps/create-category.html', context)
    def post(self, request):
        form = CategoryCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully created new category")
            return redirect('admin-page')

        context = {'form': form}
        return render(request, 'apps/create-category.html', context)

class UpdateCategory(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return render(self.request, 'apps/not-authorized.html')
    
    model = Category
    form_class = CategoryCreationForm
    template_name = 'apps/create-category.html'
    success_url = reverse_lazy('admin-page')

class AddToCartView(View):
    def post(self, request, item_id):
        if not request.user.is_authenticated:
            return redirect("login")

        item = get_object_or_404(Item, id=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item
            )
        
        if not created:
            cart_item.quantity += 1

        cart_item.save()
        return redirect('cart-page')
    
class CartView(ListView):
    model = CartItem
    template_name = 'apps/cart.html'

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        items = CartItem.objects.filter(cart=cart)

        total = sum(item.item.discounted_price * item.quantity for item in items)
        context['total'] = total
        return context
    
class DeleteCartView(DeleteView):
    model=CartItem
    success_url = reverse_lazy('cart-page')
    template_name = 'apps/confirm_delete.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
class UpdateCartItem(View):
    def post(self, request, pk):
        action = request.POST.get('action')
        item = get_object_or_404(
            CartItem, id=pk, cart__user=request.user
        )
        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        return redirect('cart-page')
"""   
class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.item.discounted_price * item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total': total
            }
        return render(request, 'apps/checkout.html', context)
    
    def post(self, request):
        phone = request.POST.get('phone')
        total = request.session.get('total')

        response = lipa_na_mpesa(phone, total)

        if response.get('ResponseCode') == '0':
            messages.success(request, 'STK Push sent. Check you phone.')
        else:
            messages.error(request, 'Payment Failed. Try again')

        return redirect('checkout')
    
class MpesaCallbackView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            result = data['Body']['stkCallback']
            result_code = result['ResultCode']

            if result_code == 0:
                metadata = result['CallbackMetadata']['Item']
                amount = next(item['value'] for item in metadata if item['Name'] == 'Amount')
                phone = next(item['Value'] for item in metadata if item['Name'] == 'PhoneNumber')

                print("Payment Success:", phone, amount)
            else:
                print("Pyament Failed")
        except Exception as e:
    
            print('Error:', str(e))
        return JsonResponse({'status': 'ok'})
"""