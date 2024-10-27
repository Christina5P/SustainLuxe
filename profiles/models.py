from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils import timezone
from decimal import Decimal
from products.models import Product as ProductsProduct
from simple_history.models import HistoricalRecords


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


class Product(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='profile_products',
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

    def update_balance(self, sale_amount):
        self.balance += Decimal(sale_amount) * Decimal('0.7')
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
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    withdrawal_history = models.JSONField(default=list, blank=True)
    history = HistoricalRecords(
        history_id_field=models.AutoField(primary_key=True)
    )

    def calculate_balance(self):
        # Beräkna totala intäkter
        sold_products = ProductsProduct.objects.filter(user=self.user, sold=True)
        total_revenue = sum(product.price for product in sold_products) * Decimal('0.7')

        # Beräkna totalen av alla uttag
        total_withdrawals = sum(Decimal(entry['amount']) for entry in self.withdrawal_history)

        # Beräkna och returnera aktuell balans
        return total_revenue - total_withdrawals

    def withdrawal(self, amount):
        amount = Decimal(amount).quantize(Decimal("0.01"))
        available_balance = self.calculate_balance()

        if amount <= self.calculate_balance():
            self.withdrawal_history.append({
                'amount': float(amount),
                'date': timezone.now().isoformat()
            })
            self.save()
            return True
        return False

    def __str__(self):
        return self.user.username
