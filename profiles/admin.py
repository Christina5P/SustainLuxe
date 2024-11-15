from django.contrib import admin
from django.utils.html import format_html
from .models import Account
from simple_history.admin import SimpleHistoryAdmin
import json
# from django import forms
from django.shortcuts import render
# from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from .forms import WithdrawalForm
from django.utils import timezone
# from django.contrib import messages


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

    actions = ['request_payout_action', 'process_pending_payout']

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
        
    def request_payout_action(self, request, queryset):
        
        if 'apply' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
               
                amount = form.cleaned_data['amount']
                bank_account_number = form.cleaned_data['bank_account_number']
                
                for account in queryset:

                    account.bank_account_number = bank_account_number

                    account.pending_payout = amount

                    account.payout_status = 'pending'
                    account.payout_requested_at = timezone.now()  

                    # Spara kontot
                    account.save()

                self.message_user(
                    request,
                    f"Payout request created for {account.user.username}.",
                   )
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = WithdrawalForm()
            return render(
                request,
                'admin/request_payout.html',
                {'form': form, 'accounts': queryset},
            )

    request_payout_action.short_description = "Request payout for selected account"

    def process_payout(self):
        """Process for request withdrawal"""
        if isinstance(self.withdrawal_history, str):
            try:
                self.withdrawal_history = json.loads(self.withdrawal_history)
            except json.JSONDecodeError:
               
                self.withdrawal_history = []

        if self.pending_payout > 0:
            for withdrawal in reversed(self.withdrawal_history):
                if withdrawal.get('status') == 'pending':
                   
                    withdrawal['status'] = 'completed'
                    withdrawal['processed_date'] = timezone.now().isoformat()
                    break

            self.total_revenue -= self.pending_payout
            self.pending_payout = 0
            self.payout_requested_at = None

            self.withdrawal_history = json.dumps(self.withdrawal_history)
            self.save()
            return True
        return False

    def process_pending_payout(self, request, queryset):
        """Process for payout to several accounts"""
        updated_count = 0
        for account in queryset:
            
            if account.process_payout():
                
                updated_count += 1
            else:
                self.message_user(request, f"Processed {updated_count} payouts.")
        if updated_count == 0:
            self.message_user(request, "No payouts were processed.")
        else:
            self.message_user(request, f"Processed payout for {updated_count} account(s).")

    def payout_status_display(self, obj):
        """Display 'Pending' if there's a pending payout, otherwise 'Completed'"""
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if obj.pending_payout > 0 else 'green',
            'Pending' if obj.pending_payout > 0 else 'Completed',
        )

    payout_status_display.short_description = 'Payout Status'

    def formatted_withdrawal_history(self, obj):
       
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
       
        return formatted_history if formatted_history else "No withdrawal history"
