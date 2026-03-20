from django.contrib import admin
from .models import Admin, Category, Client, Item

# Register your models here.
admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Item)
