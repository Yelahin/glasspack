from django.contrib import admin
from .models import UserMessage

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    readonly_fields = ["full_name", "email", "user", "date", "comment"]
    list_display = ['full_name', 'email', 'date']
    list_display_links = ['full_name', 'email', 'date']
    ordering = ['-date']
    list_per_page = 20
    search_fields = ['full_name', 'email']