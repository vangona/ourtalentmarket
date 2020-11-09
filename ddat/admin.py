from django.contrib import admin
from .models import Market, Wants

# Register your models here.


class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "admin",
        "market_name",
        "registered_dttm",
        "id",
    )


admin.site.register(Market, MarketAdmin)


class WantsAdmin(admin.ModelAdmin):
    list_display = ("summary", "index_name_w", "registered_dttm")


admin.site.register(Wants, WantsAdmin)
