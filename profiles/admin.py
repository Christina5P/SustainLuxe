from django.contrib import admin


# Register your models here.

from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'seller_balance')
    search_fields = ('user__username', 'full_name', 'email')
