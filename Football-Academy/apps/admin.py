from django.contrib import admin
from .models import Coach, Player, Contract, Skills, Position, Club

# Register your models here.
admin.site.register(Club)
admin.site.register(Coach)
admin.site.register(Contract)
admin.site.register(Player)
admin.site.register(Position)
admin.site.register(Skills)