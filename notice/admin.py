from django.contrib import admin
from .models import NoticeModel, MainModel

# Register your models here.


class NoticeModelAdmin(admin.ModelAdmin):
    list_display = ("title", "content")


admin.site.register(NoticeModel, NoticeModelAdmin)


class MainModelAdmin(admin.ModelAdmin):
    list_display = ("notice", "talentmarket", "handcraft", "group")


admin.site.register(MainModel, MainModelAdmin)
