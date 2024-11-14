from django.contrib import admin
from django.utils.html import format_html
from .models import Account
from simple_history.admin import SimpleHistoryAdmin
import json


class PayoutStatusFilter(admin.SimpleListFilter):
    title = 'Payout Status'
    parameter_name = 'payout_status'

    def lookups(self, request, model_admin):
        return (
            ('pending', 'Pending'),
            ('completed', 'Completed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(payout_status='pending')
        if self.value() == 'completed':
            return queryset.filter(payout_status='completed')
        return queryset


@admin.register(Account)
class AccountAdmin(SimpleHistoryAdmin):
    list_display = (
        'user',
        'current_balance',
        'pending_payout',
        'payout_status_display',
        'bank_account_number',
    )
    readonly_fields = (
        'formatted_withdrawal_history',
        'current_balance',
    )
    list_filter = (
        'pending_payout',
        'payout_status',
        PayoutStatusFilter,
    )
    actions = ['process_payouts']

    fieldsets = (
        (
            'Account Information',
            {
                'fields': (
                    'user',
                    'current_balance',
                    'bank_account_number',
                )
            },
        ),
        (
            'Payout Information',
            {
                'fields': (
                    'pending_payout',
                    'payout_requested_at',
                    'payout_status',
                ),
            },
        ),
        (
            'Withdrawal History',
            {'fields': ('formatted_withdrawal_history',)},
        ),
    )

    def current_balance(self, obj):
        balance = obj.calculate_balance()
        return balance

    def payout_status_display(self, obj):
        """Display 'Pending' if there's a pending payout, otherwise 'Completed'."""
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if obj.pending_payout > 0 else 'green',
            'Pending' if obj.pending_payout > 0 else 'Completed',
        )

    payout_status_display.short_description = 'Payout Status'

    def process_payouts(self, request, queryset):
        for account in queryset:
            if account.process_payout():
                self.message_user(
                    request, f'Payout processed for {account.user.username}.'
                )
            else:
                self.message_user(
                    request,
                    f'No pending payout for {account.user.username}.',
                    level='warning',
                )

    process_payouts.short_description = 'Process Pending Payouts'

    def formatted_withdrawal_history(self, obj):
        """Return formatted withdrawal history for display in Django admin."""
        if isinstance(obj.withdrawal_history, str):
            try:
                withdrawal_history = json.loads(obj.withdrawal_history)
            except json.JSONDecodeError:
                withdrawal_history = []
        else:
            withdrawal_history = obj.withdrawal_history or []

        formatted_history = "\n".join(
            [
                f"Date: {entry.get('date')}, Amount: {entry.get('amount')}, Status: {entry.get('status')}"
                for entry in withdrawal_history
            ]
        )
        return (
            formatted_history if formatted_history else "No withdrawal history"
        )

    formatted_withdrawal_history.short_description = (
        "Formatted Withdrawal History"
    )
