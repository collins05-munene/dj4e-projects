from django.shortcuts import render
from django.views import View
from .models import Item, Client, Admin

# Create your views here.
class Homepage(View):
    def get(self, request):
        items = Item.objects.all()
        context = {'items': items}
        return render(request, 'apps/homepage.html', context)

