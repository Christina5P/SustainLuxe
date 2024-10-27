from django.contrib import admin
from .models import UserProfile, Account
from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html


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


@admin.register(Account)
class AccountAdmin(SimpleHistoryAdmin):
    list_display = ('user', 'total_revenue', 'current_balance')
    readonly_fields = ('formatted_withdrawal_history', 'current_balance')

    def current_balance(self, obj):
        return obj.calculate_balance()

    current_balance.short_description = 'Current Balance'

    def formatted_withdrawal_history(self, obj):
        withdrawals = obj.withdrawal_history or []
        if not withdrawals:
            return "No withdrawal history."

        table_rows = "".join(
            f"<tr><td>{w['date']}</td><td>{w['amount']}</td></tr>"
            for w in sorted(withdrawals, key=lambda x: x['date'], reverse=True)
        )

        return format_html(
            f"""
            <table style="width:100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px;">Date</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Amount</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        """
        )

    formatted_withdrawal_history.short_description = 'Withdrawal History'

    fieldsets = (
        (
            'Withdrawal History',
            {'fields': ('formatted_withdrawal_history', 'current_balance')},
        ),
    )
