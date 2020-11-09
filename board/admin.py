from django.contrib import admin
from .models import Questions, Content, Image, Answer

# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image


class ContentAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ("title", "description")


admin.site.register(Content, ContentAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("title", "usernickname", "id")


admin.site.register(Questions, QuestionsAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("title", "id")


admin.site.register(Answer, AnswerAdmin)
