from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils import timezone
from decimal import Decimal
from products.models import Product 
from simple_history.models import HistoricalRecords
import json


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history, account and status
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    total_revenue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return self.user.username


class Sale(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sale',
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    default_phone_number = models.CharField(max_length=25, null=False, blank=False)
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

    def update_balance(self, earned_amount):
        self.balance += Decimal(earned_amount) * Decimal('0.7')
        self.save()

    def __str__(self):
        return f'{self.user.username} - Balance: {self.balance}'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    withdrawal_history = models.JSONField(default=list, blank=True)
    history = HistoricalRecords(
        history_id_field=models.AutoField(primary_key=True)
    )
    pending_payout = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
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
        try:
            withdrawal_history = json.loads(self.withdrawal_history) if self.withdrawal_history else []
        except json.JSONDecodeError:
            print(f"Kunde inte avkoda withdrawal_history: {self.withdrawal_history}")
            withdrawal_history = []

        total_withdrawals = sum(
            Decimal(w.get('amount', 0))
            for w in withdrawal_history
            if isinstance(w, dict) and w.get('status') == 'completed'
        )
        return self.total_revenue - total_withdrawals

    def request_payout(self, amount):
        amount = Decimal(amount).quantize(Decimal("0.01"))
        if amount <= self.calculate_balance():
            withdrawal_entry = {
                'amount': float(amount),
                'date': timezone.now().isoformat(),
                'status': 'pending',
            }

            current_history = (
                json.loads(self.withdrawal_history)
                if self.withdrawal_history
                else []
            )
        
            current_history.append(withdrawal_entry)

            self.withdrawal_history = json.dumps(current_history)
            self.save()
            return True
        return False

    def load_withdrawal_history(self):
        self.withdrawal_history = json.loads(self.withdrawal_history)    

    def get_pending_requests(self):
        pending_requests = []
        for w in self.withdrawal_history:
            if isinstance(w, dict) and 'status' in w:
                if w['status'] == 'pending':
                    pending_requests.append(w)
        return pending_requests

    def process_payout(self):
        if self.pending_payout > 0:
            for withdrawal in reversed(self.withdrawal_history):
                if withdrawal['status'] == 'pending':
                    withdrawal['status'] = 'completed'
                    withdrawal['processed_date'] = timezone.now().isoformat()
                    break

            self.pending_payout = 0
            self.payout_requested_at = None
            self.withdrawal_history = json.dumps(self.withdrawal_history)
            self.save()
            return True
        return False

