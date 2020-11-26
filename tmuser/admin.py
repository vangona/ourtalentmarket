from django.contrib import admin
from .models import Tmuser, WaitingId

# Register your models here.


class TmuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'useremail')


admin.site.register(Tmuser, TmuserAdmin)


class WaitingIdAdmin(admin.ModelAdmin):
    list_display = ('waiting_user',)


admin.site.register(WaitingId, WaitingIdAdmin)
