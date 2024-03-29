from django.contrib import admin
from .models import Board_Model, Game_Model, Player_Model

# Register your models here.
admin.site.register(Board_Model)
admin.site.register(Game_Model)
admin.site.register(Player_Model)
