from django.contrib import admin
from .models import TalentMarket, Handcraft, Group

# Register your models here.


class TalentMarketAdmin(admin.ModelAdmin):
    list_display = ("admin", "market_name", "registered_dttm")


admin.site.register(TalentMarket, TalentMarketAdmin)


class HandcraftAdmin(admin.ModelAdmin):
    list_display = ("admin", "market_name", "registered_dttm")


admin.site.register(Handcraft, HandcraftAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ("admin", "market_name", "registered_dttm")


admin.site.register(Group, GroupAdmin)
