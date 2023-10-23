from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin

from .models import User

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.register(User, CustomUserAdmin)
