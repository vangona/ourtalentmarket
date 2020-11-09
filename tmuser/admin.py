from django.contrib import admin
from .models import Tmuser

# Register your models here.

class TmuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'useremail')


admin.site.register(Tmuser, TmuserAdmin)
