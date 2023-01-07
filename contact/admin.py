from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Contact)

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created")

