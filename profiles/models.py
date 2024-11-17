from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from decimal import Decimal
from simple_history.models import HistoricalRecords
import json


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history, account and status
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=50, null=True, blank=True)
    default_email = models.EmailField(max_length=254, null=False, blank=False)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_country = CountryField(
        blank_label='Country', null=True, blank=True
    )

    def __str__(self):
        return self.user.username


class Sale(models.Model):
    """  For user selling products """
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sale',
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    default_phone_number = models.CharField(
        max_length=25, null=False, blank=False
    )
    default_street_address1 = models.CharField(
        max_length=80, null=False, blank=False
    )
    default_postcode = models.CharField(max_length=20, null=False, blank=False)
    default_town_or_city = models.CharField(
        max_length=40, null=False, blank=False
    )
    default_country = CountryField(
        blank_label='Country', null=False, blank=False
    )
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def update_balance_and_revenue(self, earned_amount):
        """Update both balance in Sale and total_revenue in Account."""

        earned_amount = Decimal(earned_amount) * Decimal('0.7')
        self.balance += earned_amount
        self.save()

        if hasattr(
            self.user, 'account'
        ):
            account = self.user.account
            account.total_revenue += earned_amount
            account.save()


class Account(models.Model):
    """ Users account for revenue and product status"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(
        max_digits=10, decimal_places=0, default=0.00
    )
    withdrawal_history = models.JSONField(default=list, blank=True)
    history = HistoricalRecords(
        history_id_field=models.AutoField(primary_key=True)
    )
    pending_payout = models.DecimalField(
        max_digits=10, decimal_places=0, default=0
    )
    payout_requested_at = models.DateTimeField(null=True, blank=True)
    payout_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending',
    )
    bank_account_number = models.CharField(
        max_length=255, blank=True, null=True
    )

    def calculate_balance(self):
        """Calculate the available balance by subtracting completed withdrawals """
        if isinstance(self.withdrawal_history, str):
            try:
                self.withdrawal_history = json.loads(self.withdrawal_history)
            except json.JSONDecodeError:

                self.withdrawal_history = []

        total_withdrawals = sum(
            Decimal(w.get('amount', 0))
            for w in self.withdrawal_history
            if w.get('status') == 'completed'
        )

        balance = self.total_revenue - total_withdrawals
        return balance

    def update_total_revenue(self, earned_amount):
        """Update total revenue after a sale."""
        self.total_revenue += earned_amount
        self.save()

    def request_payout(self, amount):

        if isinstance(self.withdrawal_history, str):
            try:
                self.withdrawal_history = json.loads(self.withdrawal_history)
            except json.JSONDecodeError:
                self.withdrawal_history = []

        if amount <= self.calculate_balance():
            withdrawal_entry = {
                'amount': float(amount),
                'date': timezone.now().isoformat(),
                'status': 'pending',
                'bank_account_number': self.bank_account_number,
            }

            self.withdrawal_history.append(withdrawal_entry)
            self.pending_payout += Decimal(amount)
            self.withdrawal_history = json.dumps(
                self.withdrawal_history
            )
            self.save()
            return True
        return False

    def get_pending_requests(self):

        if isinstance(self.withdrawal_history, str):
            try:
                self.withdrawal_history = json.loads(self.withdrawal_history)
            except json.JSONDecodeError:
                print(
                    f"Error decoding withdrawal_history for user {self.user.username}"
                )
                self.withdrawal_history = []

        pending_requests = [
            w for w in self.withdrawal_history if w.get('status') == 'pending'
        ]
        return pending_requests

    def process_payout(self):

        if isinstance(self.withdrawal_history, str):
            try:
                self.withdrawal_history = json.loads(self.withdrawal_history)
            except json.JSONDecodeError:
                print(
                    f"Error decoding withdrawal_history for user {self.user.username}")
                self.withdrawal_history = []

        if self.pending_payout > 0:
            for withdrawal in reversed(self.withdrawal_history):
                if withdrawal.get('status') == 'pending':
                    withdrawal['status'] = 'completed'
                    withdrawal['processed_date'] = timezone.now().isoformat()
                    break

            self.pending_payout = 0
            self.payout_requested_at = None
            self.withdrawal_history = json.dumps(self.withdrawal_history)
            self.save()

        return self.withdrawal_history
