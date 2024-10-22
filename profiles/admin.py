
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_full_name', 'get_email', 'phone_number', 'street_address1', 'postcode', 'town_or_city', 'country', 'total_revenue')
    list_filter = ('country',)
    search_fields = ('user__username', 'user__email', 'phone_number', 'street_address1', 'postcode', 'town_or_city')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'email')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'street_address1', 'postcode', 'town_or_city', 'country')
        }),
        ('Financial Information', {
            'fields': ('total_revenue',)
        }),
    )

    readonly_fields = ('user', 'total_revenue')
        
    """
        def get_user_balance(self, obj):
            return obj.user_balance  # Anta att user_balance är ett fält i UserProfile-modellen
        get_user_balance.short_description = 'User Balance'
        Lägg till get_user_balance i list display senare
    """